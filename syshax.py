from tcpgecko import TCPGecko
tcp = TCPGecko("10.0.0.2")
# make sure to check if your title exists, or else it will crash!
# if it exists, it will return 1
SYSCheckTitleExists = tcp.get_symbol("sysapp.rpl", "SYSCheckTitleExists")
# first argument is the first 32-bit set of the Title ID
# second argument is the second 32-bit set of the Title ID
# for example, this is Wooly World (USA)
SYSCheckTitleExists(0x0005000, 0x10184D00)
# now here is the title id that you will launch
# remember to have the game / disc in!!!!!
SYSLaunchTitle(0x0005000, 0x10184D00)
tcp.s.close()
print("Game switched!")
