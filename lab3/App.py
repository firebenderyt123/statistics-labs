from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from Diagnoser import Diagnoser

class App:

	def __init__(self):
		self.diagnoser = Diagnoser()

		self.root = Tk()
		self.root.title("Lab3a")
		self.generateMainFrame()

	def run(self):
		self.root.mainloop()

	def generateMainFrame(self):
		mainframe = ttk.Frame(self.root, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		# loaders
		ttk.Button(mainframe, text="Load Ascariasis", command=self.loadAscariasis).grid(column=1, row=1, sticky=N)
		ttk.Button(mainframe, text="Load Hepatitis", command=self.loadHepatitis).grid(column=2, row=1, sticky=N)
		ttk.Button(mainframe, text="Load Stones", command=self.loadStones).grid(column=3, row=1, sticky=N)

		# Inputs
		ageVar = IntVar()
		ttk.Label(mainframe, text="Age: ").grid(column=1, row=2, sticky=(W, E))
		self.ageEntry = ttk.Entry(mainframe, width=7, textvariable=ageVar)
		self.ageEntry.grid(column=2, row=2, columnspan=2, sticky=(W, E))

		nauseaVar = StringVar()
		ttk.Label(mainframe, text="Nausea: ").grid(column=1, row=3, sticky=(W, E))
		self.nauseaEntry = ttk.Entry(mainframe, width=7, textvariable=nauseaVar)
		self.nauseaEntry.grid(column=2, row=3, columnspan=2, sticky=(W, E))

		yellowishnessVar = StringVar()
		yellowishnessVar.set('eye')
		ttk.Label(mainframe, text="Yellowishness: ").grid(column=1, row=4, sticky=(W, E))
		self.yellowishnessEntry = ttk.Entry(mainframe, width=7, textvariable=yellowishnessVar)
		self.yellowishnessEntry.grid(column=2, row=4, columnspan=2, sticky=(W, E))

		rightsidepainVar = StringVar()
		rightsidepainVar.set('no')
		ttk.Label(mainframe, text="Rightside pain: ").grid(column=1, row=5, sticky=(W, E))
		self.rightsidepainEntry = ttk.Entry(mainframe, width=7, textvariable=rightsidepainVar)
		self.rightsidepainEntry.grid(column=2, row=5, columnspan=2, sticky=(W, E))

		liverenlargementVar = StringVar()
		liverenlargementVar.set('no')
		ttk.Label(mainframe, text="Liver enlargement: ").grid(column=1, row=6, sticky=(W, E))
		self.liverenlargementEntry = ttk.Entry(mainframe, width=7, textvariable=liverenlargementVar)
		self.liverenlargementEntry.grid(column=2, row=6, columnspan=2, sticky=(W, E))

		appetiteVar = StringVar()
		appetiteVar.set('yes')
		ttk.Label(mainframe, text="Appetite: ").grid(column=1, row=7, sticky=(W, E))
		self.appetiteEntry = ttk.Entry(mainframe, width=7, textvariable=appetiteVar)
		self.appetiteEntry.grid(column=2, row=7, columnspan=2, sticky=(W, E))

		# calc Button
		ttk.Button(mainframe, text="Defaults", command=self.getDefaults).grid(column=1, row=8, columnspan=1, sticky=N)
		ttk.Button(mainframe, text="Calculate", command=self.calc).grid(column=3, row=8, sticky=N)

		# results
		self.resultsLabel = ttk.Label(mainframe, text="Here you'll see results")
		self.resultsLabel.grid(column=4, row=1, columnspan=3, rowspan=8, sticky=(W, E))


		for child in mainframe.winfo_children():
			child.grid_configure(padx=5, pady=5)

	def loadAscariasis(self):
		filename = askopenfilename()
		self.diagnoser.setPath(0, filename)

	def loadHepatitis(self):
		filename = askopenfilename()
		self.diagnoser.setPath(1, filename)

	def loadStones(self):
		filename = askopenfilename()
		self.diagnoser.setPath(2, filename)

	def getDefaults(self):
		self.ageEntry.delete(0, END)
		self.ageEntry.insert(END, 12)
		self.nauseaEntry.delete(0, END)
		self.nauseaEntry.insert(END, 'no')
		self.yellowishnessEntry.delete(0, END)
		self.yellowishnessEntry.insert(END, 'eye')
		self.rightsidepainEntry.delete(0, END)
		self.rightsidepainEntry.insert(END, 'no')
		self.liverenlargementEntry.delete(0, END)
		self.liverenlargementEntry.insert(END, 'no')
		self.appetiteEntry.delete(0, END)
		self.appetiteEntry.insert(END, 'yes')

	def parseParams(self):
		return [
			int(self.ageEntry.get()), # age
			self.nauseaEntry.get(), # nausea
			self.yellowishnessEntry.get(), # yellowishness
			self.rightsidepainEntry.get(), # right_side_pain
			self.liverenlargementEntry.get(), # liver_enlargement
			self.appetiteEntry.get() # appetite
		]

	def calc(self):
		self.diagnoser.calcStatistics()
		params = self.parseParams()
		diagnoses = self.diagnoser.getDiagnose(params)
		self.resultsLabel['text'] = self.diagnoser.getTextDiagnose(diagnoses)
		self.diagnoser.drawPlot(diagnoses)

if __name__ == '__main__':
	app = App()
	app.run()

	# skin
	# liver - yes, it's Hepatit