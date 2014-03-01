import os
for i in range(1,24):
  os.system('convert hface0.gif -background white -rotate ' + str(i*15) + ' hface' + str(i) + '.gif')
