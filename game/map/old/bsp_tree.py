#!/usr/bin/python3
# Generator stems from Urizne, and are written by Vermux, slightly altered by Entikan.
# https://github.com/vurmux/urizen
#
#                                 Apache License
#                           Version 2.0, January 2004

from collections import defaultdict
import random
from uuid import uuid4
from .tile import TileWall, TileSpace



def bsp_tree(w=30, h=30, optimal_block_size=4):
    M = defaultdict(TileWall)
    nodes = {}
    root = BSPNode('v', 1, 1, w - 1, h - 1)
    _recursive_split_tree_node(root, optimal_block_size)
    _load_leafs(root, nodes)
    _fill_rooms(M, nodes.values())
    all_edges = _get_all_edges(nodes.values())
    st_edges = _construct_spanning_tree(list(nodes.keys()), all_edges)
    _create_corridors(M, nodes, st_edges)
    root.tiles = M
    return root


class BSPNode(object):
    """
    Class for BSP-tree nodes.
    """

    def __init__(self, xy_type, x, y, w, h, children=None):
        # UUID
        self.uid = uuid4()

        # Type of node
        # 'v' means that this node should be splitted vertically
        # 'h' means that this node should be splitted horizontally
        self.xy_type = xy_type

        # Parameters of the BSP block
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Parameters of the room inside the block, if exists
        self.room_x1 = None
        self.room_y1 = None
        self.room_x2 = None
        self.room_y2 = None

        # Node children, if exists
        self.children = children

    def create_room(self):
        self.room_x1 = random.randint(
            int(self.x + 0.1 * self.w),
            int(self.x + 0.2 * self.w)
        )
        self.room_y1 = random.randint(
            int(self.y + 0.1 * self.h),
            int(self.y + 0.2 * self.h)
        )
        self.room_x2 = random.randint(
            int(self.x + 0.8 * self.w),
            int(self.x + 0.9 * self.w)
        )
        self.room_y2 = random.randint(
            int(self.y + 0.8 * self.h),
            int(self.y + 0.9 * self.h)
        )

    def get_leaf(self, x, y):
        for leaf in self.leafs.values():
            if x >= leaf.room_x1 and x < leaf.room_x2:
                if y >= leaf.room_y1 and y < leaf.room_y2:
                    return leaf
                

def _recursive_split_tree_node(bsp_node, optimal_block_size):
    """
    Make binary space partitioning of the map.

    Partitioning stops when the current node has width/height no more than
    1.5 of the `optimal_block_size` and width/height no more than twice larger
    than height/width.
    """

    if bsp_node.xy_type == 'v':
        if bsp_node.w > int(optimal_block_size * 1.5) or bsp_node.w > 2 * bsp_node.h:
            w_child = random.randint(int(bsp_node.w * 0.25), int(bsp_node.w * 0.75))
            child_left = BSPNode(
                'h',
                bsp_node.x,
                bsp_node.y,
                w_child,
                bsp_node.h
            )
            child_right = BSPNode(
                'h',
                bsp_node.x + w_child,
                bsp_node.y,
                bsp_node.w - w_child,
                bsp_node.h
            )
            bsp_node.children = [child_left, child_right]
            _recursive_split_tree_node(child_left, optimal_block_size)
            _recursive_split_tree_node(child_right, optimal_block_size)
        else:
            bsp_node.create_room()
    elif bsp_node.xy_type == 'h':
        if bsp_node.h > int(optimal_block_size * 1.5) or bsp_node.h > 2 * bsp_node.w:
            h_child = random.randint(int(bsp_node.h * 0.25), int(bsp_node.h * 0.75))
            child_top = BSPNode(
                'v',
                bsp_node.x,
                bsp_node.y,
                bsp_node.w,
                h_child
            )
            child_bottom = BSPNode(
                'v',
                bsp_node.x,
                bsp_node.y + h_child,
                bsp_node.w,
                bsp_node.h - h_child
            )
            bsp_node.children = [child_top, child_bottom]
            _recursive_split_tree_node(child_top, optimal_block_size)
            _recursive_split_tree_node(child_bottom, optimal_block_size)
        else:
            bsp_node.create_room()


def _load_leafs(bsp_node, leafs):
    """
    Collect all leaf nodes in the BSP-tree and put them in the list.
    """

    if bsp_node.children:
        _load_leafs(bsp_node.children[0], leafs)
        _load_leafs(bsp_node.children[1], leafs)
    else:
        leafs[bsp_node.uid] = bsp_node
    bsp_node.leafs = leafs


def _fill_rooms(M, nodes):
    """
    Fill map with rooms given from leaf nodes of BSP-tree.
    """

    for node in nodes:
        for y in range(node.room_y1, node.room_y2):
            for x in range(node.room_x1, node.room_x2):
                M[x, y] = TileSpace()


def _get_all_edges(bsp_nodes):
    """
    Get all possible straight edges between rooms in leaf nodes of BSP-tree.
    """

    all_edges = []
    for n1 in bsp_nodes:
        for n2 in bsp_nodes:
            if n1.uid == n2.uid:
                continue
            n1_x2 = n1.x + n1.w
            n1_y2 = n1.y + n1.h
            n2_x2 = n2.x + n2.w
            n2_y2 = n2.y + n2.h
            max_rx1 = max(n1.room_x1, n2.room_x1)
            max_ry1 = max(n1.room_y1, n2.room_y1)
            min_rx2 = min(n1.room_x2, n2.room_x2)
            min_ry2 = min(n1.room_y2, n2.room_y2)
            if ((n1.y == n2_y2 or n1_y2 == n2.y) and
                    (max_rx1 < min_rx2) and
                    min(n1_x2, n2_x2) - max(n1.x, n2.x) > 0.6 * min(n1.w, n2.w)):
                all_edges.append((n1.uid, n2.uid))
            elif ((n1.x == n2_x2 or n1_x2 == n2.x) and
                    (max_ry1 < min_ry2) and
                    min(n1_y2, n2_y2) - max(n1.y, n2.y) > 0.6 * min(n1.h, n2.h)):
                all_edges.append((n1.uid, n2.uid))
    return all_edges


def _construct_spanning_tree(nodes, edges):
    """
    Construct spanning tree of edges graph using Prim's
    (also known as Jarník's) algorithm.
    """

    nodes_to_process = set(nodes)
    first_edge = random.choice(edges)
    st_nodes = [first_edge[0], first_edge[1]]
    st_edges = [first_edge]
    nodes_to_process.remove(first_edge[0])
    nodes_to_process.remove(first_edge[1])
    tries = 0
    while nodes_to_process:
        node_uid = random.choice(st_nodes)
        for edge in filter(lambda e: node_uid in e, edges):
            second_node_uid = (
                edge[0]
                if node_uid == edge[1]
                else edge[1]
            )
            if second_node_uid in nodes_to_process:
                st_nodes.append(second_node_uid)
                st_edges.append(edge)
                nodes_to_process.remove(second_node_uid)
                break
        tries += 1
        print(tries)
    return st_edges


def _create_corridors(M, nodes, edges):
    """
    Create corridors between rooms that should be connected.
    """

    for edge in edges:
        n1 = nodes[edge[0]]
        n2 = nodes[edge[1]]
        if max(n1.room_x1, n2.room_x1) < min(n1.room_x2-1, n2.room_x2-1):
            x = random.randint(
                max(n1.room_x1, n2.room_x1),
                min(n1.room_x2-1, n2.room_x2-1)
            )
            for y in range(min(n2.room_y2-1, n1.room_y1), max(n2.room_y2-1, n1.room_y1)):
                M[x, y] = TileSpace()
        elif max(n1.room_y1, n2.room_y1) < min(n1.room_y2-1, n2.room_y2-1):
            y = random.randint(
                max(n1.room_y1, n2.room_y1),
                min(n1.room_y2-1, n2.room_y2-1)
            )
            for x in range(min(n2.room_x2-1, n1.room_x1), max(n2.room_x2-1, n1.room_x1)):
                M[x, y] = TileSpace()
