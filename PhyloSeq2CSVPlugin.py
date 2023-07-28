import PyPluMA
import PyIO

TAX=["","(Kingdom)","(Phylum)","(Class)","(Order)","(Family)","(Genus)","(Species)"]

class PhyloSeq2CSVPlugin:
    def input(self, infile):
       self.parameters = PyIO.readParameters(infile)
       self.abundancefile = open(PyPluMA.prefix()+"/"+self.parameters["abundance"], 'r')
       self.taxonomyfile = open(PyPluMA.prefix()+"/"+self.parameters["taxonomy"], 'r')
       self.level = int(self.parameters["level"])
       self.concatenate = True
       if ('concatenate' in self.parameters and self.parameters['concatenate'] == "False"):
           self.concatenate = False

    def run(self):
        # Build updated taxonomy.  Assumption is that the first column is the
        # name, followed by kingdom, phylum, etc.
        # Mapping will go from unique name to taxonomy at level, if not NA
        # Otherwise, the next highest with a qualifier
        self.taxonomyfile.readline()
        self.classifications = dict()
        for line in self.taxonomyfile:
            contents = line.strip().split(',')
            myname = contents[0]
            levels = len(contents)
            i=1
            while (i <= self.level and i < levels and contents[i] != "\"NA\""):
                i += 1
            # The first element to the left is the classification
            classidx = i
            if (i == levels or (i-1) == self.level or contents[i] == "\"NA\""):
                classidx -= 1
            myclass = contents[classidx]
            if (i-1 != self.level):
               myclass = TAX[i-1] + " " + myclass
            elif (self.level == 7):
               if (self.concatenate):
                myclass = contents[6][:len(contents[6])-1] + "_" + contents[7][1:]
               else:
                myclass = '\"' + contents[7][1:]
            self.classifications[myname] = myclass
        # Build updated abundance table.  Assumption is that the first
        # column is the name, followed by abundances in each sample.
        # File should be padded.
        self.samples = self.abundancefile.readline().strip().split(',')
        self.samples = self.samples[1:]
        self.abundances = dict()
        for line in self.abundancefile:
           contents = line.strip().split(',')
           name = contents[0]
           myclass = self.classifications[name]
           abundancevalues = contents[1:]
           for i in range(len(abundancevalues)):
               abundancevalues[i] = float(abundancevalues[i])
           if (myclass in self.abundances):
               for i in range(len(self.abundances[myclass])):
                   self.abundances[myclass][i] += abundancevalues[i]
           else:
               self.abundances[myclass] = abundancevalues

    def output(self, outfilename):
       outfile = open(outfilename, 'w')
       outfile.write("\"\",")
       for i in range(len(self.samples)):
           outfile.write(self.samples[i])
           if (i != len(self.samples)-1):
               outfile.write(',')
           else:
               outfile.write('\n')
       for name in self.abundances:
           outfile.write(name)
           outfile.write(',')
           for i in range(len(self.abundances[name])):
               outfile.write(str(self.abundances[name][i]))
               if (i != len(self.abundances[name])-1):
                   outfile.write(',')
               else:
                   outfile.write('\n')


