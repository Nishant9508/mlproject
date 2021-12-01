import cv2
import numpy as np
import time

# Code for Kyeframe Extraction
def framing():
	frames = []
	canned_frames = []
	cap = cv2.VideoCapture('C:/Users/ASUS/Documents/Dev/Assigment_ngo/Video_1.mp4')
	
	timestamp = [0.0]
	fps = cap.get(cv2.CAP_PROP_FPS)

	while (cap.isOpened()):
		frame_exists, curr_frame = cap.read()
		if frame_exists == True:
			cv2.resize(curr_frame, (2000,2000), interpolation=cv2.INTER_CUBIC)
			cv2.imshow("Video", curr_frame)
			grayed = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
			canned = cv2.Canny(grayed, 320, 320)
			frames.append(curr_frame)
			canned_frames.append(canned)
			timestamp.append(timestamp[-1] + 1000/fps)
			k = cv2.waitKey(10) & 0XFF
			if k == ord('q'):
				break
		else:
			break
	cap.release()
	cv2.destroyAllWindows()
	return canned_frames, frames, timestamp 

canned_frames, original_frames, timestamp = framing()
cv2.destroyAllWindows()

timestamp_sec= []
for time in timestamp:
	timestamp_sec.append("{:.2f}".format(time/1000))

abs_diff = []
for i in range(0, len(canned_frames)-1):
	abs_diff.append(cv2.absdiff(canned_frames[i], canned_frames[i+1]))

overall_mean = np.mean(abs_diff)
overall_standarddev = np.std(abs_diff)

a = 4
overall_thresh = overall_mean + (a * overall_standarddev)

actual_frames = []
for i in range(len(abs_diff)):
	mn = np.mean(abs_diff[i])
	st_d = np.std(abs_diff[i])
	fr_ts = mn + (4*st_d)
	actual_frames.append([i, fr_ts])

imp_fr = []
for i, ac_tr in (actual_frames):
	if ac_tr >= overall_thresh:
		imp_fr.append([i, ac_tr])


key_frames = []
key_timestamps = []
for i, _ in imp_fr:
	key_frames.append(original_frames[i])
	key_timestamps.append(timestamp_sec[i])
print("Timestamps of the key frames")
print()
print(key_timestamps)

#Code for Yolov3 object detection and identifying frames having most number of objects

curr_objects = 0
max_objects = 0

confThreshold = 0.4  
nmsThreshold = 0.4   


classes = open('C:/Users/ASUS/Documents/Dev/YOLO_v3/coco.names').read().strip().split('\n')

net = cv2.dnn.readNetFromDarknet(r'C:\Users\ASUS\Documents\Dev\YOLO_v3\yolov3-tiny.cfg',r'C:\Users\ASUS\Documents\Dev\YOLO_v3\yolov3-tiny.weights',)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def getOutputsNames(net):
	layersNames = net.getLayerNames()
	return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]

def drawPred(classId, conf, left, top, right, bottom):
	cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

	label = '%.2f' % conf

	if classes:
		assert(classId < len(classes))
		label = '%s:%s' % (classes[classId], label)

	#Display the label at the top of the bounding box
	labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
	top = max(top, labelSize[1])
	cv2.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv2.FILLED)
	cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

def postprocess(frame, outp):
	frameHeight = frame.shape[0]
	frameWidth = frame.shape[1]

	classIds = []
	confidences = []
	boxes = []
	for out in outp:
		for detection in out:
			scores = detection[5:]
			classId = np.argmax(scores)
			confidence = scores[classId]
			if confidence > confThreshold:
				center_x = int(detection[0] * frameWidth)
				center_y = int(detection[1] * frameHeight)
				width = int(detection[2] * frameWidth)
				height = int(detection[3] * frameHeight)
				left = int(center_x - width / 2)
				top = int(center_y - height / 2)
				classIds.append(classId)
				confidences.append(float(confidence))
				boxes.append([left, top, width, height])


	indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
	for i in indices:
		box = boxes[i]
		left = box[0]
		top = box[1]
		width = box[2]
		height = box[3]
		drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
	curr = len(indices)
	return curr

for i in range(len(key_frames)):

	frame = key_frames[i]

	blob = cv2.dnn.blobFromImage(frame, 1/255, (316,316), [0,0,0], 1, crop=False)

	net.setInput(blob)

	outp = net.forward(getOutputsNames(net))

	curr_objects = postprocess(frame, outp)

	if(curr_objects>max_objects):
		max_objects = curr_objects
		index_max = i
	cv2.imshow('Image', frame)
	cv2.waitKey(5)
cv2.destroyAllWindows()	
cv2.imshow('Final Image having maximun objects ', key_frames[index_max])
cv2.waitKey(0)
print("Timestamp of frame having most number of objects is : " + str(key_timestamps[index_max]) + " sec")