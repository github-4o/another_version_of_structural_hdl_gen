from src.test_nodes.Test_top_structural_node import Test_top_structural_node


def dump_files(hdl):
    print(hdl)
    for i in hdl:
        print("writing file ", i[0])
        with open("output/"+i[0], "w") as f:
            f.write(i[1])

top_node=Test_top_structural_node()

dump_files(top_node.dump_hdl())

print("done")
