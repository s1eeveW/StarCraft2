import mpyq
# from s2protocol import versions

# Using mpyq, load the replay file.
archive = mpyq.MPQArchive('D:/SC2/SC/56003.SC2Replay')

contents = archive.header['user_data_header']['content']
# print(NNet.Game.SChatMessage)
# Now parse the header information.
# header = versions.latest().decode_replay_headesr(contents)