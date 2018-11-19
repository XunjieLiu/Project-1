import threading
import time

myLock = threading.RLock()
num = 0

class myThread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name

	def run(self):
		global num

		while True:
			myLock.acquire()
			print("\nThread(%s) locked, Number: %d" % (self.name, num))

			if num >= 10:
				myLock.release()
				print("\nThread(%s) released, Number: %d" % (self.name, num))
				break

			num+=1
			print("\nThread(%s) released, Number: %d" % (self.name, num))
			myLock.release()

			time.sleep(2)



def test():
	thread1 = myThread("A")
	thread2 = myThread("B")

	thread1.start()
	thread2.start()

if __name__ == '__main__':
	test()