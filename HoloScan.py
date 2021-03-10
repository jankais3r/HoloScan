import os
import ui
import sys
import math
import time
import shutil
import socket
import dialogs
import console
import zipfile
import urllib.request
from objc_util import *
from threading import Event, Thread
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
try:
	import diff_match_patch
except:
	for pth in sys.path:
		if pth[-15:] == 'site-packages-3':
			sp3 = pth + '/'
	with urllib.request.urlopen('https://files.pythonhosted.org/packages/c2/5a/9aa3b95a1d108b82fadb1eed4c3773d19069f765bd4c360a930e107138ee/diff_match_patch-20200713-py3-none-any.whl') as f:
		with open(sp3 + 'dmp.zip', 'wb') as ff:
			ff.write(f.read())
	with zipfile.ZipFile(sp3 + 'dmp.zip') as zf:
		zf.extractall(sp3)
	shutil.rmtree(sp3 + 'diff_match_patch-20200713.dist-info', ignore_errors = True)
	os.remove(sp3 + 'dmp.zip')
	import diff_match_patch

if os.path.isfile('holoplay.js'):
	with open('holoplay.js', 'r') as f:
		holoplay_js = f.read()
else:
	with urllib.request.urlopen('https://cdn.jsdelivr.net/npm/holoplay@0.2.3/holoplay.js') as f:
		holoplay_js_vanilla = f.read().decode('utf-8')
	
	with urllib.request.urlopen('https://raw.githubusercontent.com/jankais3r/driverless-HoloPlay.js/main/holoplay.js.patch') as f:
		diff = f.read().decode('utf-8').replace('\r\n', '\n')
	dmp = diff_match_patch.diff_match_patch()
	patches = dmp.patch_fromText(diff)
	holoplay_js, _ = dmp.patch_apply(patches, holoplay_js_vanilla)
	holoplay_js = holoplay_js.replace(
	# Original calibration:
	'{"configVersion":"1.0","serial":"00000","pitch":{"value":49.825218200683597},"slope":{"value":5.2160325050354},"center":{"value":-0.23396748304367066},"viewCone":{"value":40.0},"invView":{"value":1.0},"verticalAngle":{"value":0.0},"DPI":{"value":338.0},"screenW":{"value":2560.0},"screenH":{"value":1600.0},"flipImageX":{"value":0.0},"flipImageY":{"value":0.0},"flipSubp":{"value":0.0}}',
	# Your calibration:
	'{"configVersion":"1.0","serial":"00000","pitch":{"value":47.56401443481445},"slope":{"value":-5.480000019073486},"center":{"value":0.374184787274007},"viewCone":{"value":40.0},"invView":{"value":1.0},"verticalAngle":{"value":0.0},"DPI":{"value":338.0},"screenW":{"value":2560.0},"screenH":{"value":1600.0},"flipImageX":{"value":0.0},"flipImageY":{"value":0.0},"flipSubp":{"value":0.0}}')
	with open('holoplay.js', 'w') as f:
		f.write(holoplay_js)

if os.path.isfile('three.min.js'):
	with open('three.min.js', 'r') as f:
		three_js = f.read()
else:
	with urllib.request.urlopen('https://cdn.jsdelivr.net/gh/mrdoob/three.js@r124/build/three.min.js') as f:
		three_js = f.read().decode('utf-8')
	with open('three.min.js', 'w') as f:
		f.write(three_js)

if os.path.isfile('OrbitControls.js'):
	with open('OrbitControls.js', 'r') as f:
		orbitcontrols_js = f.read()
else:
	with urllib.request.urlopen('https://cdn.jsdelivr.net/gh/mrdoob/three.js@r124/examples/js/controls/OrbitControls.js') as f:
		orbitcontrols_js = f.read().decode('utf-8').replace('this.getPolarAngle = function () {', '''
	this.pan = function ( deltaX, deltaY ) {

		pan( deltaX, deltaY );
		scope.update();

	};

	this.dollyIn = function() {

		dollyIn( getZoomScale() );
		scope.update();

	};

	this.dollyOut = function() {

		dollyOut( getZoomScale() );
		scope.update();

	};

	this.rotateLeft = function( angle ) {

		rotateLeft( angle );
		scope.update();

	};

	this.rotateUp = function( angle ) {

		rotateUp( angle );
		scope.update();

	};

	this.getPolarAngle = function () {''')
	with open('OrbitControls.js', 'w') as f:
		f.write(orbitcontrols_js)

if os.path.isfile('PLYLoader.js'):
	with open('PLYLoader.js', 'r') as f:
		PLYLoader_js = f.read()
else:
	with urllib.request.urlopen('https://cdn.jsdelivr.net/gh/mrdoob/three.js@r124/examples/js/loaders/PLYLoader.js') as f:
		PLYLoader_js = f.read().decode('utf-8').replace('var geometry;', '').replace('“', '').replace('”', '')
	with open('PLYLoader.js', 'w') as f:
		f.write(PLYLoader_js)

class Handler(BaseHTTPRequestHandler):
	@on_main_thread
	def do_GET(self):
		global scanPointCountLabel, scenePointCountLabel, reducedPointCount, wk, scaniverseFix, hegesFix
		if self.path.endswith('scan.ply'):
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			with open(filename, 'rb') as f:
				self.wfile.write(f.read())
			return
		
		elif self.path.endswith('holoplay.js'):
			self.send_response(200)
			self.send_header('Content-type', 'text/javascript')
			self.end_headers()
			self.wfile.write((holoplay_js).encode())
			return
		
		elif self.path.endswith('three.min.js'):
			self.send_response(200)
			self.send_header('Content-type', 'text/javascript')
			self.end_headers()
			self.wfile.write((three_js).encode())
			return
		
		elif self.path.endswith('OrbitControls.js'):
			self.send_response(200)
			self.send_header('Content-type', 'text/javascript')
			self.end_headers()
			self.wfile.write((orbitcontrols_js).encode())
			return
		
		elif self.path.endswith('PLYLoader.js'):
			self.send_response(200)
			self.send_header('Content-type', 'text/javascript')
			self.end_headers()
			self.wfile.write((PLYLoader_js).encode())
			return
		
		elif self.path.startswith('/delegate'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(''.encode())
			delegateString = self.path.replace('/delegate', '')
			if delegateString.startswith('scanpoints'):
				reducedPointCount = int(float(delegateString[10:]))
				scanPointCountLabel.text = format(reducedPointCount, ',d')
				if comments == 'EM3D':
					wk.evaluateJavaScript_completionHandler_('''
					geometry.attributes.position.array = geometry.attributes.position.array.map(x => x * 5);
					origGeometry.attributes.position.array = origGeometry.attributes.position.array.map(x => x * 5);
					geometry.attributes.position.needsUpdate = true;
					particles.rotation.y = THREE.Math.degToRad(180);''', None)
				elif comments == 'Heges':
					wk.evaluateJavaScript_completionHandler_('particles.rotation.x = THREE.Math.degToRad(-15);', None)
					# Uncomment when viewing TrueDepth scans
					# wk.evaluateJavaScript_completionHandler_('''
					# geometry.attributes.position.array = geometry.attributes.position.array.map(x => x * 5);
					# origGeometry.attributes.position.array = origGeometry.attributes.position.array.map(x => x * 5);
					# geometry.attributes.position.needsUpdate = true;''', None)
				if comments == 'ScandyPro':
					wk.evaluateJavaScript_completionHandler_('''
					geometry.attributes.position.array = geometry.attributes.position.array.map(x => x * 8);
					origGeometry.attributes.position.array = origGeometry.attributes.position.array.map(x => x * 8);
					geometry.attributes.position.needsUpdate = true;
					particles.rotation.y = THREE.Math.degToRad(180);''', None)
				elif comments == 'Scaniverse':
					wk.evaluateJavaScript_completionHandler_('particles.rotation.x = THREE.Math.degToRad(' + str(scaniverseFix) + ');', None)
			elif delegateString.startswith('scenepoints'):
				reducedPointCount = int(float(delegateString[11:]))
				if (reducedPointCount * trimSlider.value < reducedPointCount * (1 - seekSlider.value)):
					scenePointCountLabel.text = format(int(float(reducedPointCount * trimSlider.value)), ',d')
				else:
					scenePointCountLabel.text = format(int(float(reducedPointCount * (1 - seekSlider.value))), ',d')
				if comments == 'Heges':
					if hegesFix == 0:
						reductionSelect(None)
						hegesFix = 1
			elif delegateString.startswith('nocolor'):
				colorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(1)
				colorSelector.objc_instance.segmentedControl().setEnabled_forSegmentAtIndex_(0, 0)
				if comments == 'Scaniverse':
					scaniverseFix = 0
			elif delegateString.startswith('reducefactor'):
				reduceFactor = int(delegateString[12:])
				if reduceFactor == 1:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(0)
				elif reduceFactor == 2:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(1)
				elif reduceFactor == 5:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(2)
				elif reduceFactor == 10:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(3)
				elif reduceFactor == 25:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(4)
				elif reduceFactor == 50:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(5)
				elif reduceFactor == 100:
					reductionFactorSelector.objc_instance.segmentedControl().setSelectedSegmentIndex_(6)
				customFactorInput.text = str(reduceFactor)
			return
		
		elif self.path.endswith('cameracontrol.html'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write((control_html).encode())
			return
		
		elif self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(scene_html.encode())
			return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

class Server():
	server = None
	def start_server(self):
		self.server = ThreadedHTTPServer(('0.0.0.0', 8080), Handler)
		server_thread = Thread(target = self.server.serve_forever)
		server_thread.daemon = False
		server_thread.start()
	
	def stop_server(self):
		self.server.shutdown()
		self.server.server_close()

class UIView(ui.View):
	def get_key_commands(self):
		return [{'input': 'UIKeyInputUpArrow'}, {'input': 'UIKeyInputDownArrow'}, {'input': 'UIKeyInputLeftArrow'}, {'input': 'UIKeyInputRightArrow'}, {'input': 'UIKeyInputUpArrow', 'modifiers':'cmd'}, {'input': 'UIKeyInputDownArrow', 'modifiers':'cmd'}, {'input': 'UIKeyInputLeftArrow', 'modifiers':'cmd'}, {'input': 'UIKeyInputRightArrow', 'modifiers':'cmd'}, {'input': 'UIKeyInputUpArrow', 'modifiers':'shift'}, {'input': 'UIKeyInputDownArrow', 'modifiers':'shift'}, {'input': 'UIKeyInputLeftArrow', 'modifiers':'shift'}, {'input': 'UIKeyInputRightArrow', 'modifiers':'shift'}, {'input': 'UIKeyInputUpArrow', 'modifiers':'cmd,shift'}, {'input': 'UIKeyInputDownArrow', 'modifiers':'cmd,shift'}, {'input': 'UIKeyInputLeftArrow', 'modifiers':'cmd,shift'}, {'input': 'UIKeyInputRightArrow', 'modifiers':'cmd,shift'}]
		
	def key_command(self, sender):
		global cameraControl
		# print('key_command='+str(sender))
		if sender['input'] == 'up':
			if sender['modifiers'] == '':
				cameraControl.evaluate_javascript('controls.pan(0, 10);')
			elif sender['modifiers'] == 'cmd':
				cameraControl.evaluate_javascript('controls.dollyOut();')
			elif sender['modifiers'] == 'shift':
				cameraControl.evaluate_javascript('controls.rotateUp(THREE.Math.degToRad(5));')
			elif sender['modifiers'] == 'cmd,shift':
				cameraControl.evaluate_javascript('mesh.position.y -= 0.5;')
				wk.evaluateJavaScript_completionHandler_('particles.position.y -= 0.5;', None)
		if sender['input'] == 'down':
			if sender['modifiers'] == '':
				cameraControl.evaluate_javascript('controls.pan(0, -10);')
			elif sender['modifiers'] == 'cmd':
				cameraControl.evaluate_javascript('controls.dollyIn();')
			elif sender['modifiers'] == 'shift':
				cameraControl.evaluate_javascript('controls.rotateUp(THREE.Math.degToRad(-5));')
			elif sender['modifiers'] == 'cmd,shift':
				cameraControl.evaluate_javascript('mesh.position.y += 0.5;')
				wk.evaluateJavaScript_completionHandler_('particles.position.y += 0.5;', None)
		if sender['input'] == 'left':
			if sender['modifiers'] == '':
				cameraControl.evaluate_javascript('controls.pan(10, 0);')
			elif sender['modifiers'] == 'cmd':
				cameraControl.evaluate_javascript('controls.autoRotateSpeed = 2; controls.autoRotate = true; controls.update();')
			elif sender['modifiers'] == 'shift':
				cameraControl.evaluate_javascript('controls.rotateLeft(THREE.Math.degToRad(5));')
			elif sender['modifiers'] == 'cmd,shift':
				cameraControl.evaluate_javascript('mesh.rotation.z -= THREE.Math.degToRad(10);')
				wk.evaluateJavaScript_completionHandler_('particles.rotation.z -= THREE.Math.degToRad(10);', None)
		if sender['input'] == 'right':
			if sender['modifiers'] == '':
				cameraControl.evaluate_javascript('controls.pan(-10, 0);')
			elif sender['modifiers'] == 'cmd':
				cameraControl.evaluate_javascript('controls.autoRotateSpeed = -2; controls.autoRotate = true; controls.update();')
			elif sender['modifiers'] == 'shift':
				cameraControl.evaluate_javascript('controls.rotateLeft(THREE.Math.degToRad(-5));')
			elif sender['modifiers'] == 'cmd,shift':
				cameraControl.evaluate_javascript('mesh.rotation.z += THREE.Math.degToRad(10);')
				wk.evaluateJavaScript_completionHandler_('particles.rotation.z += THREE.Math.degToRad(10);', None)

class debugDelegate(object):
	def webview_should_start_load(self, webview, url, nav_type):
		global wk
		try:
			if url.startswith('camera'):
				val = urllib.parse.unquote(url)[7:].split('|')
				wk.evaluateJavaScript_completionHandler_('camera.position.x = ' + val[0] + '; camera.position.y = ' + val[1] + ';camera.position.z = ' + val[2], None)
				wk.evaluateJavaScript_completionHandler_('var vector = new THREE.Vector3(' + val[3] + ', ' + val[4] + ', ' + val[5] + '); camera.lookAt(vector.add(camera.position));', None)
			return True
		except:
			return True

class customFactorDelegate(object):
	def select_all(self):
		tf = ObjCInstance(customFactorInput).subviews()[0]
		start_pos = tf.beginningOfDocument()
		end_pos = tf.endOfDocument()
		range = tf.textRangeFromPosition_toPosition_(start_pos, end_pos)
		tf.setSelectedTextRange_(range)
	
	def textfield_did_begin_editing(self, textfield):
		ui.delay(self.select_all, 0)
	
	def textfield_did_end_editing(self, textfield):
		global wk, customFactorInput
		if textfield.text.isdigit() == True:
			if int(textfield.text) >= 1:
				customFactorInput.border_color = '#e3e3e3'
				try:
					wk.evaluateJavaScript_completionHandler_('reduce(' + textfield.text + ');', None)
					wk.evaluateJavaScript_completionHandler_('geometry.setDrawRange( geometry.attributes.position.count * ' + str(seekSlider.value) + ', geometry.attributes.position.count * ' + str(trimSlider.value) + ' );', None)
					wk.evaluateJavaScript_completionHandler_('report.delegate("scenepoints" + geometry.attributes.position.count );', None)
					if colorSelector.selected_index == 1:
						wk.evaluateJavaScript_completionHandler_('geometry.attributes.color.array.fill( 1 ); geometry.attributes.color.needsUpdate = true;', None)
					elif colorSelector.selected_index == 2:
						wk.evaluateJavaScript_completionHandler_(depthmap_js, None)
				except:
					pass
		else:
			customFactorInput.border_color = 'red'

scene_html = '''
<!DOCTYPE html>
<html>
	<head>
	<style>
		html,
		body {
			margin: 0;
		}
	</style>
		<meta charset="utf-8">
	</head>
	<body>
		<script src="http://localhost:8080/three.min.js"></script>
		<script src="http://localhost:8080/OrbitControls.js"></script>
		<script src="http://localhost:8080/PLYLoader.js"></script>
		<script src="http://localhost:8080/holoplay.js"></script>
		<script>
			report = new Object();
			report.delegate = function(log) {
				var iframe = document.createElement("IFRAME");
				iframe.setAttribute("src", "http://localhost:8080/delegate" + log);
				document.documentElement.appendChild(iframe);
				setTimeout(function() {
					iframe.parentNode.removeChild(iframe);
					iframe = null;
				}, 1000);
			};
		
			var container;
			var camera, scene, renderer, controls, holoplay;
			var geometry, origGeometry, origPosCount, particles;
			
			init();
			render();
			
			function reduce(reductionFactor) {
				var newPosCount = Math.floor(origPosCount / reductionFactor);
				var newPositions = new Float32Array( newPosCount * 3 );
				var newColors = new Float32Array( newPosCount * 3 );
				
				for (i = 0; i < newPosCount * 3; i += 3) {
					newPositions[i] = origGeometry.attributes.position.array[i * reductionFactor];
					newPositions[i + 1] = origGeometry.attributes.position.array[i * reductionFactor + 1];
					newPositions[i + 2] = origGeometry.attributes.position.array[i * reductionFactor + 2];
					newColors[i] = origGeometry.attributes.color.array[i * reductionFactor];
					newColors[i + 1] = origGeometry.attributes.color.array[i * reductionFactor + 1];
					newColors[i + 2] = origGeometry.attributes.color.array[i * reductionFactor + 2];
				}
				geometry.deleteAttribute( 'position' );
				geometry.setAttribute( 'position', new THREE.BufferAttribute( newPositions, 3 ) );
				geometry.deleteAttribute( 'color' );
				geometry.setAttribute( 'color', new THREE.BufferAttribute( newColors, 3 ) );
				
				particles.geometry.center();
			}

			function init() {
				container = document.createElement( 'div' );
				document.body.appendChild( container );
				camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 1500 );
				camera.position.set(0, 0, 10);
				camera.lookAt(0, 0, 0);
				scene = new THREE.Scene();
				
				var material;
				var planeMaterial;
				const loader = new THREE.PLYLoader();
				loader.load( 'http://localhost:8080/scan.ply', function ( geometry ) {
					if (geometry.attributes.color === undefined) {
						var fakeColor = new Float32Array( geometry.attributes.position.array.length );
						fakeColor.fill( 1 );
						geometry.setAttribute( 'color', new THREE.BufferAttribute( fakeColor, 3 ) );
						report.delegate("nocolor");
					}
					//geometry.deleteAttribute( 'normal' );
					origGeometry = geometry.clone();
					origPosCount = origGeometry.attributes.position.count;
					report.delegate("scanpoints" + origPosCount);
					
					material = new THREE.PointsMaterial({ vertexColors: true, size: 0.01 });
					particles = new THREE.Points(geometry, material);
					
					//particles.geometry.center();
					
					const ratios = [1, 2, 5, 10, 25, 50, 100];
					const target = geometry.attributes.position.count / 130000;
					const closest = ratios.find(e => e >= target);
					reduce(closest);
					
					scene.add(particles);
					
					report.delegate("reducefactor" + closest);
					report.delegate("scenepoints" + geometry.attributes.position.count);
					}
				);
				
				renderer = new THREE.WebGLRenderer( { powerPreference: "high-performance" } );
				renderer.setPixelRatio( window.devicePixelRatio );
				renderer.setSize( window.innerWidth, window.innerHeight );
				container.appendChild( renderer.domElement );
				
				holoplay = new HoloPlay(scene, camera, renderer);
				
				window.addEventListener( 'resize', onWindowResize );
			}

			function onWindowResize() {
				camera.aspect = window.innerWidth / window.innerHeight;
				camera.updateProjectionMatrix();
				renderer.setSize( window.innerWidth, window.innerHeight );
			}

			function render() {
				requestAnimationFrame( render );
				holoplay.render();
			}
		</script>
	</body>
</html>
'''

control_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		html,
		body {
			margin: 0;
		}
	</style>
	<meta charset="utf-8" />
</head>
<body>
	<script src="http://localhost:8080/three.min.js"></script>
	<script src="http://localhost:8080/OrbitControls.js"></script>
	<script>
		report = new Object();
		report.camera = function(log) {
			var iframe = document.createElement("IFRAME");
			iframe.setAttribute("src", "camera:" + log);
			document.documentElement.appendChild(iframe);
			iframe.parentNode.removeChild(iframe);
			iframe = null;
		};
		var camera, scene, renderer, controls, mesh;

		function init() {
			scene = new THREE.Scene();
			camera = new THREE.PerspectiveCamera(35, window.innerWidth / window.innerHeight, 1, 1500);
			camera.position.set(0, 0, 10);
			renderer = new THREE.WebGLRenderer();
			renderer.setSize(window.innerWidth, window.innerHeight);
			document.body.appendChild(renderer.domElement);
			controls = new THREE.OrbitControls(camera, renderer.domElement);
			controls.addEventListener("change", report_camera);
			controls.addEventListener("start", function(){controls.autoRotate = false;});
			mesh = new THREE.Mesh(new THREE.SphereGeometry(1, 8, 8), new THREE.MeshBasicMaterial({
				color: 0xffffff,
				wireframe: true
			}));
			scene.add(mesh);
		}

		window.addEventListener("resize", function() {
			var width = window.innerWidth;
			var height = window.innerHeight;
			renderer.setSize(width, height);
			camera.aspect = width / height;
			camera.updateProjectionMatrix();
		});

		function render() {
			requestAnimationFrame(render);
			renderer.render(scene, camera);
			controls.update();
		}

		function report_camera() {
			var camerastring = camera.position.x + '|' + camera.position.y + '|' + camera.position.z + '|' + camera.getWorldDirection().x + '|' + camera.getWorldDirection().y + '|' + camera.getWorldDirection().z
			report.camera(camerastring);
		}

		init();
		render();
	</script>
</body>
</html>
'''

depthmap_js = '''
var minx = 0;
var miny = 0;
var minz = 0;
var maxx = 0;
var maxy = 0;
var maxz = 0;

for (i = 0; i < geometry.attributes.position.count * 3; i += 3) {
	if (geometry.attributes.position.array[i] < minx) {
		minx = geometry.attributes.position.array[i];
	}
	if (geometry.attributes.position.array[i + 1] < miny) {
		miny = geometry.attributes.position.array[i + 1];
	}
	if (geometry.attributes.position.array[i + 2] < minz) {
		minz = geometry.attributes.position.array[i + 2];
	}
	if (geometry.attributes.position.array[i] > maxx) {
		maxx = geometry.attributes.position.array[i];
	}
	if (geometry.attributes.position.array[i + 1] > maxy) {
		maxy = geometry.attributes.position.array[i + 1];
	}
	if (geometry.attributes.position.array[i + 2] > maxz) {
		maxz = geometry.attributes.position.array[i + 2];
	}
}

for (i = 0; i < geometry.attributes.position.count * 3; i += 3) {
	var cx = geometry.attributes.position.array[i];
	var cy = geometry.attributes.position.array[i + 1];
	var cz = geometry.attributes.position.array[i + 2];
	
	geometry.attributes.color.array[i] = 0.7 * (cx + Math.abs(minx)) / maxx;
	geometry.attributes.color.array[i + 1] = 0.7 * (cy + Math.abs(miny)) / maxy;
	geometry.attributes.color.array[i + 2] = 0.7 * (cz + Math.abs(minz)) / maxz;
}
geometry.attributes.color.needsUpdate = true;
'''

wk = None
reducedPointCount = None
scaniverseFix = 270
hegesFix = 0

@on_main_thread
def main():
	global wk
	UIScreen = ObjCClass('UIScreen')
	
	if len(UIScreen.screens()) > 1:
		secondScreen = UIScreen.screens()[1]
		secondScreen.overscanCompensation = 0
		bounds = secondScreen.bounds()

		UIWindow = ObjCClass('UIWindow')
		secondWindow = UIWindow.alloc().initWithFrame_(bounds)
		secondWindow.setScreen(secondScreen)
		secondWindow.makeKeyAndVisible()
		
		wk = ObjCClass('WKWebView').alloc().initWithFrame_(CGRect((0, 0), (secondScreen.bounds().size.width, secondScreen.bounds().size.height - 1))).autorelease()
		secondWindow.addSubview(wk)
		
		request = ObjCClass('NSURLRequest').alloc().init()
		urlns = nsurl('http://localhost:8080')
		x = request.initWithURL_(urlns)
		wk.loadRequest_(x)
		
		windows = ObjCClass('UIApplication').sharedApplication()
		for window in windows.windows():
			if 'PA3PythonistaWindow' in str(window._get_objc_classname()):
				window.makeKeyAndVisible()
	else:
		print('No secondary screen detected. Connect your Looking Glass.')
		v.close()
		s.stop_server()
		quit()

def disable_swipe_to_close(view):
	UILayoutContainerView = ObjCClass('UILayoutContainerView')
	UISwipeGestureRecognizer = ObjCClass('UISwipeGestureRecognizer')
	v = view.objc_instance
	while not v.isKindOfClass_(UILayoutContainerView.ptr):
		v = v.superview()
	for gr in v.gestureRecognizers():
		if gr.isKindOfClass_(UISwipeGestureRecognizer.ptr):
			gr.setEnabled(False)

def reductionSelect(sender):
	global wk, customFactor
	try:
		if reductionFactorSelector.selected_index == 0:
			customFactorInput.alpha = 0
			customFactorInput.text = '1'
			wk.evaluateJavaScript_completionHandler_('reduce(1);', None)
		elif reductionFactorSelector.selected_index == 1:
			customFactorInput.alpha = 0
			customFactorInput.text = '2'
			wk.evaluateJavaScript_completionHandler_('reduce(2);', None)
		elif reductionFactorSelector.selected_index == 2:
			customFactorInput.alpha = 0
			customFactorInput.text = '5'
			wk.evaluateJavaScript_completionHandler_('reduce(5);', None)
		elif reductionFactorSelector.selected_index == 3:
			customFactorInput.alpha = 0
			customFactorInput.text = '10'
			wk.evaluateJavaScript_completionHandler_('reduce(10);', None)
		elif reductionFactorSelector.selected_index == 4:
			customFactorInput.alpha = 0
			customFactorInput.text = '25'
			wk.evaluateJavaScript_completionHandler_('reduce(25);', None)
		elif reductionFactorSelector.selected_index == 5:
			customFactorInput.alpha = 0
			customFactorInput.text = '50'
			wk.evaluateJavaScript_completionHandler_('reduce(50);', None)
		elif reductionFactorSelector.selected_index == 6:
			customFactorInput.alpha = 0
			customFactorInput.text = '100'
			wk.evaluateJavaScript_completionHandler_('reduce(100);', None)
		elif reductionFactorSelector.selected_index == 7:
			customFactorInput.alpha = 1
			customFactorInput.begin_editing()
		if colorSelector.selected_index == 1:
			wk.evaluateJavaScript_completionHandler_('geometry.attributes.color.array.fill( 1 ); geometry.attributes.color.needsUpdate = true;', None)
		elif colorSelector.selected_index == 2:
			wk.evaluateJavaScript_completionHandler_(depthmap_js, None)
		wk.evaluateJavaScript_completionHandler_('geometry.setDrawRange( geometry.attributes.position.count * ' + str(seekSlider.value) + ', geometry.attributes.position.count * ' + str(trimSlider.value) + ' );', None)
		wk.evaluateJavaScript_completionHandler_('report.delegate("scenepoints" + geometry.attributes.position.count )', None)
	except:
		pass

def colorSelect(sender):
	global wk, customFactorInput
	if colorSelector.selected_index == 0:
		wk.evaluateJavaScript_completionHandler_('''
		for (i = 0; i < geometry.attributes.color.count * 3; i += 3) {
			geometry.attributes.color.array[i] = origGeometry.attributes.color.array[i * ''' + customFactorInput.text + '''];
			geometry.attributes.color.array[i + 1] = origGeometry.attributes.color.array[i * ''' + customFactorInput.text + ''' + 1];
			geometry.attributes.color.array[i + 2] = origGeometry.attributes.color.array[i * ''' + customFactorInput.text + ''' + 2];
		}
		geometry.attributes.color.needsUpdate = true;
		''', None)
	elif colorSelector.selected_index == 1:
		wk.evaluateJavaScript_completionHandler_('geometry.attributes.color.array.fill( 1 ); geometry.attributes.color.needsUpdate = true;', None)
	elif colorSelector.selected_index == 2:
		wk.evaluateJavaScript_completionHandler_(depthmap_js, None)

def rotateLeftAction(sender):
	global cameraControl
	cameraControl.evaluate_javascript('controls.autoRotateSpeed = 2; controls.autoRotate = true; controls.update();')

def rotateRightAction(sender):
	global cameraControl
	cameraControl.evaluate_javascript('controls.autoRotateSpeed = -2; controls.autoRotate = true; controls.update();')

def resetCameraAction(sender):
	global cameraControl, wk
	cameraControl.evaluate_javascript('mesh.position.y = 0;')
	wk.evaluateJavaScript_completionHandler_('particles.position.y = 0;', None)
	cameraControl.evaluate_javascript('mesh.rotation.z = 0;')
	wk.evaluateJavaScript_completionHandler_('particles.rotation.z = 0;', None)
	cameraControl.evaluate_javascript('''
	controls.autoRotate = false;
	controls.update();
	setTimeout(function() {
		controls.reset();
	}, 100);''')

def closeAction(sender):
	global v, wk, s
	wk.loadHTMLString_baseURL_('', None)
	wk = None
	del wk
	v.close()
	s.stop_server()
	console.clear()
	console.hide_output()
	quit()

def seekSlide(sender):
	global wk, scenePointCountLabel
	wk.evaluateJavaScript_completionHandler_('geometry.setDrawRange( geometry.attributes.position.count * ' + str(seekSlider.value) + ', geometry.attributes.position.count * ' + str(trimSlider.value) + ' );', None)
	if (reducedPointCount * trimSlider.value < reducedPointCount * (1 - seekSlider.value)):
		scenePointCountLabel.text = format(int(float(reducedPointCount * trimSlider.value)), ',d')
	else:
		scenePointCountLabel.text = format(int(float(reducedPointCount * (1 - seekSlider.value))), ',d')

def trimSlide(sender):
	global wk, scenePointCountLabel
	wk.evaluateJavaScript_completionHandler_('geometry.setDrawRange( geometry.attributes.position.count * ' + str(seekSlider.value) + ', geometry.attributes.position.count * ' + str(trimSlider.value) + ' );', None)
	if (reducedPointCount * trimSlider.value < reducedPointCount * (1 - seekSlider.value)):
		scenePointCountLabel.text = format(int(float(reducedPointCount * trimSlider.value)), ',d')
	else:
		scenePointCountLabel.text = format(int(float(reducedPointCount * (1 - seekSlider.value))), ',d')

def pointSizeSlide(sender):
	global wk
	val = (pointSizeSlider.value * pointSizeSlider.value) / 10
	wk.evaluateJavaScript_completionHandler_('particles.material.size = ' + str(val) + ' ;', None)

try:
	filename = dialogs.pick_document()
	assert filename[-4:] == '.ply'
except:
	quit()

comments = ''
with open(filename, 'r', errors = 'ignore') as f:
	try:
		for comment in f:
			if comment.startswith('comment '):
				comments = comments + comment[8:]
	except:
		pass

comments = comments.replace('\n', '')
if comments == 'Metadata { "color_space": "sRGB" }':
	comments = 'EM3D'
elif comments == 'object: defaultGroup01':
	comments = 'LiDAR Scanner 3D'
elif comments == 'PCL generated':
	comments = '3d Scanner App'
elif comments == 'VTK generated PLY File':
	comments = 'ScandyPro'
elif 'HEGE.SH' in comments:
	comments = 'Heges'
elif 'Scaniverse' in comments:
	comments = 'Scaniverse'
elif 'SiteScape' in comments:
	comments = 'SiteScape'

s = Server()
s.start_server()

scanPointsLabel = ui.Label(text = 'Scan Points', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
filenameLabel = ui.Label(text = os.path.basename(filename), font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
scenePointsLabel = ui.Label(text = 'Scene Points', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
scanPointCountLabel = ui.Label(text = 'Loading', font = ('<system>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
camImage = ui.ImageView(alpha = 0.3)
sfcam = ObjCClass('UIImage').systemImageNamed_('camera.viewfinder')
with ui.ImageContext(30, 30) as ctx:
	sfcam.drawInRect_(CGRect(CGPoint(0, 0), CGSize(30, 30)))
	camImage.image = ctx.get_image()
commentsLabel = ui.Label(text = comments, font = ('<system>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
scenePointCountLabel = ui.Label(text = 'Loading', font = ('<system>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
reductionFactorLabel = ui.Label(text = 'Point Count Reduction Factor', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
pointSizeLabel = ui.Label(text = 'Point Size', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
seekLabel = ui.Label(text = 'Seek', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
trimLabel = ui.Label(text = 'Trim', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')
colorLabel = ui.Label(text = 'Point Color', font = ('<system-bold>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black')

reductionFactorSelector = ui.SegmentedControl(corner_radius = 5)
reductionFactorSelector.segments = ('1', '2', '5', '10', '25', '50', '100', 'Other')
reductionFactorSelector.selected_index = 0
reductionFactorSelector.action = reductionSelect
customFactorInput = ui.TextField(text = '1', font = ('<system>', 14), alignment = ui.ALIGN_CENTER, text_color = 'black', border_width = 2, border_color = '#e3e3e3', corner_radius = 7, alpha = 0)
customFactorInput.delegate = customFactorDelegate()
seekSlider = ui.Slider(continuous = True, value = 0)
seekSlider.action = seekSlide
trimSlider = ui.Slider(continuous = True, value = 1)
trimSlider.action = trimSlide
pointSizeSlider = ui.Slider(continuous = True, value = 0.333)
pointSizeSlider.action = pointSizeSlide
colorSelector = ui.SegmentedControl(corner_radius = 5)
colorSelector.segments = ('True Colors', 'White', 'Depth Map')
colorSelector.selected_index = 0
colorSelector.action = colorSelect
cameraControl = ui.WebView(corner_radius = 10)
cameraControl.delegate = debugDelegate()
rotateLeftButton = ui.Button(title = '\u293e', font = ('<system>', 30), background_color = 'black', tint_color = 'white', corner_radius = 10)
rotateLeftButton.action = rotateLeftAction
resetCameraButton = ui.Button(title = 'Reset Camera', background_color = 'black', tint_color = 'white', corner_radius = 5)
resetCameraButton.action = resetCameraAction
rotateRightButton = ui.Button(title = '\u293f', font = ('<system>', 30), background_color = 'black', tint_color = 'white', corner_radius = 10)
rotateRightButton.action = rotateRightAction
closeButton = ui.Button(title = 'Close', background_color = 'black', tint_color = 'white', corner_radius = 5)
closeButton.action = closeAction

v = UIView()
v.present(style = 'fullscreen', hide_title_bar = True)
disable_swipe_to_close(v)
v.add_subview(scanPointsLabel)
v.add_subview(filenameLabel)
v.add_subview(scenePointsLabel)
v.add_subview(scanPointCountLabel)
v.add_subview(camImage)
v.add_subview(commentsLabel)
v.add_subview(scenePointCountLabel)
v.add_subview(reductionFactorLabel)
v.add_subview(reductionFactorSelector)
v.add_subview(customFactorInput)
v.add_subview(pointSizeLabel)
v.add_subview(pointSizeSlider)
v.add_subview(seekLabel)
v.add_subview(colorLabel)
v.add_subview(seekSlider)
v.add_subview(trimLabel)
v.add_subview(trimSlider)
v.add_subview(colorSelector)
v.add_subview(cameraControl)
v.add_subview(rotateLeftButton)
v.add_subview(resetCameraButton)
v.add_subview(rotateRightButton)
v.add_subview(closeButton)

scanPointsLabel.frame = (v.width / 2 - 210, 35, 100, 30)
filenameLabel.frame = (v.width / 2 - 100, 35, 200, 30)
scenePointsLabel.frame = (v.width / 2 + 107, 35, 100, 30)
scanPointCountLabel.frame = (v.width / 2 - 210, 65, 100, 30)
camImage.frame = (v.width / 2 - 9, 68, 18, 16)
commentsLabel.frame = (v.width / 2 - 110, 80, 220, 30)
scenePointCountLabel.frame = (v.width / 2 + 107, 65, 100, 30)
reductionFactorLabel.frame = (v.width / 2 - 100, 115, 200, 30)
reductionFactorSelector.frame = (v.width / 2 - 200, 155, 400, 30)
customFactorInput.frame = (v.width / 2 + 210, 155, 40, 30)
pointSizeLabel.frame = (v.width / 2 - 50, 200, 100, 30)
pointSizeSlider.frame = (v.width / 2 - 200, 225, 400, 30)
seekLabel.frame = (v.width / 2 - 50, 260, 100, 30)
seekSlider.frame = (v.width / 2 - 200, 285, 400, 30)
trimLabel.frame = (v.width / 2 - 50, 320, 100, 30)
trimSlider.frame = (v.width / 2 - 200, 345, 400, 30)
colorLabel.frame = (v.width / 2 - 200, 380, 400, 30)
colorSelector.frame = (v.width / 2 - 200, 420, 400, 30)
cameraControl.frame = (v.width / 2 - 200, 465, 400, 345)
cameraControl.load_url('http://localhost:8080/cameracontrol.html')
rotateLeftButton.frame = (v.width / 2 - 200, 780, 30, 30)
resetCameraButton.frame = (v.width / 2 - 60, 780, 120, 30)
rotateRightButton.frame = (v.width / 2 + 170, 780, 30, 30)
closeButton.frame = (v.width / 2 + 300, 50, 80, 30)

main()
try:
	# If you are rendering a complex Three.js scene and the hologram doesn't look right, try increasing the sleep timer.
	# This is a hack around a webkit bug. The window needs to be resized once the rendering completes in order to use correct shader values.
	time.sleep(3)
	wk.setFrame_(CGRect((0, 0), (secondScreen.bounds().size.width, secondScreen.bounds().size.height)))
except:
	pass
