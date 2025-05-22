import numpy as np

def read_mesh(filename):
    with open(filename, 'r') as f:
        # 判断文件类型
        tline = f.readline().strip()
        if tline != "# Created by COMSOL Multiphysics.":
            raise ValueError("File may not be a valid mphtxt file!")

        sdim = 0
        sdim_known = False
        num_nodes = 0
        num_node_known = False
        num_elements = 0
        edge_entity_ready = False
        ele_entity_ready = False

        coords = None
        surface_edge_node = None
        ele_node = None
        surface_edge_entity = None
        ele_entity = None
        num_surface_edge = 0

        count = 0

        tline = f.readline()
        while tline:
            tline = tline.strip()
            count += 1
            # 确定网格点个数
            if (not num_node_known and len(tline) > 25 and 
                tline.endswith('# number of mesh vertices')):
                num_nodes = int(tline[:-26].strip())
                num_node_known = True

            # 确定空间维度
            elif (not sdim_known and len(tline) > 6 and 
                  tline.endswith('# sdim')):
                sdim = int(tline[:-7].strip())
                sdim_known = True

            # 读取网格点坐标
            elif tline == "# Mesh vertex coordinates":
                coords = np.zeros((num_nodes, sdim))
                for i in range(num_nodes):
                    tline = f.readline().strip()
                    coords[i, :] = np.fromstring(tline, sep=' ')
            
            # 读取表面边实体编号
            elif tline == "2 # number of vertices per element":
                tline = f.readline().strip()
                num_surface_edge = int(tline[:-21].strip())
                surface_edge_node = np.zeros((num_surface_edge, 2), dtype=np.uint32)
                f.readline()  # 跳过一行
                for i in range(num_surface_edge):
                    tline = f.readline().strip()
                    surface_edge_node[i, :] = np.fromstring(tline, sep=' ', dtype=np.uint32)
                edge_entity_ready = True

            # 读取单元-结点关系
            elif tline == "3 # number of vertices per element":
                tline = f.readline().strip()
                num_elements = int(tline[:-21].strip())
                ele_node = np.zeros((num_elements, 3), dtype=np.uint32)
                f.readline()  # 跳过一行
                for i in range(num_elements):
                    tline = f.readline().strip()
                    ele_node[i, :] = np.fromstring(tline, sep=' ', dtype=np.uint32)
                ele_entity_ready = True

            elif edge_entity_ready and tline == f"{num_surface_edge} # number of geometric entity indices":
                tline = f.readline().strip()
                surface_edge_entity = np.zeros(num_surface_edge, dtype=np.uint32)
                for i in range(num_surface_edge):
                    tline = f.readline().strip()
                    surface_edge_entity[i] = int(tline)

            elif ele_entity_ready and tline == f"{num_elements} # number of geometric entity indices":
                tline = f.readline().strip()
                ele_entity = np.zeros(num_elements, dtype=np.uint32)
                for i in range(num_elements):
                    tline = f.readline().strip()
                    ele_entity[i] = int(tline)

            tline = f.readline()

    mesh = {
        'sdim': sdim,
        'num_node': num_nodes,
        'num_ele': num_elements,
        'num_surface_edge': num_surface_edge,
        'coord': coords,
        'surface_edge_node': surface_edge_node,
        'ele_node': ele_node,
        'surface_edge_entity': surface_edge_entity,
        'ele_entity': ele_entity
    }
    return mesh


def mphtxt2vtk(filename):
    """
    Convert mphtxt mesh to vtk format.
    """

    mesh = read_mesh(filename)
    
    # 创建vtk文件，使用meshio库，将它转换为vtk格式
    import meshio
    new_mesh = meshio.Mesh(
        points=mesh['coord'],
        cells={"triangle": mesh['ele_node']},
    )
    return new_mesh

if __name__ == "__main__":
    mesh = mphtxt2vtk("mesh.mphtxt")