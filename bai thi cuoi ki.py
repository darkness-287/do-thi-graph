import heapq
from collections import deque
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

adj      = {}
directed = False
capacity = {}

#  THÊM ĐỈNH / CẠNH
def them_dinh(u):
    if u not in adj:
        adj[u] = []
        print(f" Đã thêm đỉnh {u}")
    else:
        print(f" Đỉnh {u} đã tồn tại!")


def them_canh(u, v):
    if u not in adj:
        adj[u] = []
    if v not in adj:
        adj[v] = []

    if v not in adj[u]:
        adj[u].append(v)
        adj[u].sort()

    if not directed:
        if u not in adj[v]:
            adj[v].append(u)
            adj[v].sort()

    print(f" Đã thêm cạnh ({u} → {v})")


def them_canh_trong_so(u, v, w):
    
    if u not in adj:
        adj[u] = []
    if v not in adj:
        adj[v] = []

    adj[u].append((w, v))
    if not directed:
        adj[v].append((w, u))

    print(f" Đã thêm cạnh ({u} – {v}) trọng số {w}")


def them_canh_suc_chua(u, v, cap):

    if u not in adj:
        adj[u] = []
    if v not in adj:
        adj[v] = []

    if v not in adj[u]:
        adj[u].append(v)
        adj[u].sort()
    if u not in adj[v]:
        adj[v].append(u)
        adj[v].sort()

    capacity[(u, v)] = capacity.get((u, v), 0) + cap
    if (v, u) not in capacity:
        capacity[(v, u)] = 0

    print(f" Đã thêm cạnh ({u} → {v}) sức chứa {cap}")


#  BFS / DFS

def BFS(start):
    if start not in adj:
        print(f" Đỉnh {start} không tồn tại trong đồ thị!")
        return

    visited  = set()
    hang_doi = deque([start])
    thu_tu   = []
    visited.add(start)

    while hang_doi:
        u = hang_doi.popleft()
        thu_tu.append(u)
        for hang_xom in adj[u]:
            nb = hang_xom[1] if isinstance(hang_xom, tuple) else hang_xom
            if nb not in visited:
                visited.add(nb)
                hang_doi.append(nb)

    print("\n Thứ tự BFS: " + " → ".join(str(x) for x in thu_tu))
    print()


def _dfs_de_quy(u, visited, thu_tu):
    visited.add(u)
    thu_tu.append(u)
    for hang_xom in adj[u]:
        nb = hang_xom[1] if isinstance(hang_xom, tuple) else hang_xom
        if nb not in visited:
            _dfs_de_quy(nb, visited, thu_tu)


def DFS(start):
    if start not in adj:
        print(f" Đỉnh {start} không tồn tại trong đồ thị!")
        return

    visited = set()
    thu_tu  = []
    _dfs_de_quy(start, visited, thu_tu)

    print("\n Thứ tự DFS: " + " → ".join(str(x) for x in thu_tu))
    print()

# FORD-FULKERSON (LUỒNG CỰC ĐẠI)

def ford_fulkerson(source, sink):
    if source not in adj:
        print(f" Đỉnh nguồn {source} không tồn tại!")
        return
    if sink not in adj:
        print(f" Đỉnh đích {sink} không tồn tại!")
        return
    if source == sink:
        print(" Đỉnh nguồn và đỉnh đích phải khác nhau!")
        return
    if not capacity:
        print(" Chưa có cạnh nào có sức chứa! Hãy dùng lựa chọn 4 để thêm.")
        return

    cap      = dict(capacity)
    max_flow = 0
    buoc     = 0

    while True:
        parent  = {}
        visited = {source}
        queue   = deque([source])
        found   = False

        while queue and not found:
            u = queue.popleft()
            for v in adj.get(u, []):
                nb = v[1] if isinstance(v, tuple) else v
                if nb not in visited and cap.get((u, nb), 0) > 0:
                    visited.add(nb)
                    parent[nb] = u
                    if nb == sink:
                        found = True
                        break
                    queue.append(nb)

        if not found:
            break

        path_flow = float('inf')
        v = sink
        duong_di  = [v]
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, cap.get((u, v), 0))
            duong_di.append(u)
            v = u
        duong_di.reverse()

        buoc += 1
        print(f"\n Bước {buoc}: Đường tăng luồng: " +
              " → ".join(str(x) for x in duong_di) +
              f"  |  Luồng tăng thêm: {path_flow}")

        v = sink
        while v != source:
            u = parent[v]
            cap[(u, v)] = cap.get((u, v), 0) - path_flow
            cap[(v, u)] = cap.get((v, u), 0) + path_flow
            v = u

        max_flow += path_flow

    print(f"\n  Luồng cực đại từ {source} đến {sink} = {max_flow}\n")


#  CHUYỂN ĐỔI BIỂU DIỄN ĐỒ THỊ

def chuyen_doi_bieu_dien():
    if not adj:
        print(" Đồ thị đang trống!")
        return

    nodes = sorted(adj.keys(), key=str)
    idx   = {nodes[i]: i for i in range(len(nodes))}
    n     = len(nodes)

    print("\n Ma trận kề:")
    header = "     " + "  ".join(f"{str(v):>3}" for v in nodes)
    print(header)
    print("     " + "─" * (5 * n))

    matrix = [[0] * n for _ in range(n)]
    for u in nodes:
        for item in adj[u]:
            v = item[1] if isinstance(item, tuple) else item
            if v in idx:
                matrix[idx[u]][idx[v]] = 1

    for i, u in enumerate(nodes):
        row = "  ".join(f"{matrix[i][j]:>3}" for j in range(n))
        print(f" {str(u):>3} | {row}")

    print("\n Danh sách kề:")
    for u in nodes:
        hang_xom = []
        for item in adj[u]:
            v = item[1] if isinstance(item, tuple) else item
            hang_xom.append(str(v))
        print(f"   {u}  →  [{', '.join(hang_xom)}]")

    print("\n Danh sách cạnh:")
    da_luu = set()
    for u in nodes:
        for item in adj[u]:
            if isinstance(item, tuple):
                w, v = item
                canh = (str(u), str(v)) if directed else tuple(sorted([str(u), str(v)]))
                if canh not in da_luu:
                    da_luu.add(canh)
                    print(f"   ({u} – {v}, trọng số = {w})")
            else:
                v = item
                canh = (str(u), str(v)) if directed else tuple(sorted([str(u), str(v)]))
                if canh not in da_luu:
                    da_luu.add(canh)
                    mui_ten = "→" if directed else "–"
                    print(f"   ({u} {mui_ten} {v})")
    print()


#  KIỂM TRA ĐỒ THỊ 2 PHÍA

def kiem_tra_2_phia():
    if not adj:
        print(" Đồ thị đang trống!")
        return

    mau = {}

    for dinh_bat_dau in adj:
        if dinh_bat_dau in mau:
            continue
        mau[dinh_bat_dau] = 0
        hang_doi = deque([dinh_bat_dau])

        while hang_doi:
            u = hang_doi.popleft()
            for item in adj[u]:
                v = item[1] if isinstance(item, tuple) else item
                if v not in mau:
                    mau[v] = 1 - mau[u]
                    hang_doi.append(v)
                elif mau[v] == mau[u]:
                    print(" Đồ thị KHÔNG phải đồ thị 2 phía.\n")
                    return


    tap_0 = [str(v) for v in sorted(adj.keys(), key=str) if mau.get(v) == 0]
    tap_1 = [str(v) for v in sorted(adj.keys(), key=str) if mau.get(v) == 1]
    print("  Đồ thị LÀ đồ thị 2 phía!")
    print(f"   Tập X: {{{', '.join(tap_0)}}}")
    print(f"   Tập Y: {{{', '.join(tap_1)}}}\n")


#   PRIM (cây khung nhỏ nhất)

def prim(start):
    if start not in adj:
        print(f" Đỉnh {start} không tồn tại trong đồ thị!")
        return

    mau_thu = next(iter(adj[start]), None)
    if mau_thu is None or not isinstance(mau_thu, tuple):
        print(" Prim cần đồ thị có trọng số! Hãy dùng lựa chọn 3 để thêm cạnh có trọng số.")
        return

    visited  = {start}
    hang_doi = []
    for w, v in adj[start]:
        heapq.heappush(hang_doi, (w, start, v))

    mst_canh = []
    tong_w   = 0
    buoc     = 0

    print(f"\n Bắt đầu từ đỉnh: {start}")
    print(f" MST ban đầu: {{{start}}}\n")

    while hang_doi and len(visited) < len(adj):
        w, u, v = heapq.heappop(hang_doi)
        if v in visited:
            continue

        visited.add(v)
        mst_canh.append((u, v, w))
        tong_w += w
        buoc   += 1

        print(f" Bước {buoc}: Chọn cạnh ({u} – {v}), trọng số = {w}")
        print(f"          → Thêm đỉnh {v} vào MST")
        print(f"          → MST hiện tại: {sorted(visited, key=str)}\n")

        for w2, nb in adj[v]:
            if nb not in visited:
                heapq.heappush(hang_doi, (w2, v, nb))

    if len(visited) < len(adj):
        print(" Đồ thị không liên thông, MST chỉ bao gồm một phần!\n")
    else:
        print(" Hoàn tất cây khung nhỏ nhất (Prim):")

    for u, v, w in mst_canh:
        print(f"   {u} – {v}  (trọng số {w})")
    print(f"\n Tổng trọng số MST = {tong_w}\n")



#  FLEURY (chu trình / đường đi Euler)

def _dem_canh_fleury(g):
    return sum(len(v) for v in g.values()) // 2


def _xoa_canh_fleury(g, u, v):
    g[u].remove(v)
    g[v].remove(u)


def _dfs_dem_fleury(g, start, visited):
    visited.add(start)
    dem = 1
    for nb in g[start]:
        if nb not in visited:
            dem += _dfs_dem_fleury(g, nb, visited)
    return dem


def _la_cau_fleury(g, u, v):
    truoc = _dfs_dem_fleury(g, u, set())
    _xoa_canh_fleury(g, u, v)
    sau   = _dfs_dem_fleury(g, u, set())
    g[u].append(v)
    g[v].append(u)
    return sau < truoc


def _chon_dinh_bat_dau_fleury(g):
    dinh_bac_le = [v for v in g if len(g[v]) % 2 == 1]
    if len(dinh_bac_le) not in (0, 2):
        return None
    if len(dinh_bac_le) == 2:
        return dinh_bac_le[0]
    for v in g:
        if len(g[v]) > 0:
            return v
    return None


def fleury():
    if not adj:
        print(" Đồ thị đang trống!")
        return

    for u in adj:
        for item in adj[u]:
            if isinstance(item, tuple):
                print(" Fleury chỉ dùng được với đồ thị không có trọng số (cạnh thường).")
                return

    g = {u: list(adj[u]) for u in adj}

    start = _chon_dinh_bat_dau_fleury(g)
    if start is None:
        print(" Đồ thị không có đường đi Euler (số đỉnh bậc lẻ ≠ 0 hoặc 2)!\n")
        return

    current   = start
    duong_di  = [current]
    buoc      = 0

    print(f"\n Bắt đầu từ đỉnh: {start}\n")
    print(f" {'Bước':<8}{'Cạnh chọn':<20}{'Đường đi hiện tại':<35}{'Cạnh còn lại'}")
    
    while _dem_canh_fleury(g) > 0:
        hang_xom = g[current]
        if not hang_xom:
            break

        chon = hang_xom[0]
        if len(hang_xom) > 1:
            for nb in hang_xom:
                if not _la_cau_fleury(g, current, nb):
                    chon = nb
                    break

        _xoa_canh_fleury(g, current, chon)
        duong_di.append(chon)
        buoc += 1

        ten_canh   = f"{current} – {chon}"
        ten_duong  = " → ".join(str(x) for x in duong_di)
        con_lai    = _dem_canh_fleury(g)
        print(f" {buoc:<8}{ten_canh:<20}{ten_duong:<35}{con_lai}")

        current = chon
    print("\n Kết quả:")
    print("   " + " → ".join(str(x) for x in duong_di) + "\n")

#  HIERHOLZER (chu trình Euler)

def _co_euler_hierholzer():
    if not adj:
        return False

    co_canh = [u for u in adj if adj[u]]
    if not co_canh:
        return False

    visited = set()
    queue   = deque([co_canh[0]])
    visited.add(co_canh[0])
    while queue:
        u = queue.popleft()
        for item in adj[u]:
            v = item[1] if isinstance(item, tuple) else item
            if v not in visited:
                visited.add(v)
                queue.append(v)

    if any(u not in visited for u in co_canh):
        return False

    for u in adj:
        bac = 0
        for item in adj[u]:
            bac += 1
        if bac % 2 != 0:
            return False

    return True


def hierholzer():
    if not adj:
        print(" Đồ thị đang trống!")
        return

    if not _co_euler_hierholzer():
        print(" Đồ thị không có chu trình Euler!")
        print(" (Cần: đồ thị liên thông và mọi đỉnh có bậc chẵn)\n")
        return

    g = {}
    for u in adj:
        g[u] = []
        for item in adj[u]:
            v = item[1] if isinstance(item, tuple) else item
            g[u].append(v)

    stack  = [list(g.keys())[0]]
    path   = []

    while stack:
        u = stack[-1]
        if g[u]:
            v = g[u][0]
            stack.append(v)
            g[u].remove(v)
            g[v].remove(u)
        else:
            path.append(stack.pop())

    path.reverse()
    print("\n  Chu trình Euler (Hierholzer):")
    print("   " + " → ".join(str(x) for x in path) + "\n")


# luu do thi

def luu_do_thi():
    if not adj:
        print(" Đồ thị đang trống, không có gì để lưu!\n")
        return

    ten_file = input(" Nhập tên file (Enter = do_thi.txt): ").strip()
    if not ten_file:
        ten_file = "do_thi.txt"

    da_luu        = set()
    canh_thuong   = []
    canh_trong_so = []
    canh_suc_chua = []

    for u in sorted(adj.keys(), key=str):
        for item in adj[u]:
            if isinstance(item, tuple):
                w, v = item
                canh = tuple(sorted([str(u), str(v)]))
                if canh not in da_luu:
                    da_luu.add(canh)
                    canh_trong_so.append((u, v, w))
            else:
                v = item
                canh = tuple(sorted([str(u), str(v)]))
                key_ff = (u, v)
                if key_ff in capacity or (v, u) in capacity:
                    if canh not in da_luu:
                        da_luu.add(canh)
                        cap_uv = capacity.get((u, v), 0)
                        cap_vu = capacity.get((v, u), 0)
                        canh_suc_chua.append((u, v, cap_uv, cap_vu))
                else:
                    if canh not in da_luu:
                        da_luu.add(canh)
                        canh_thuong.append((u, v))

    with open(ten_file, "w", encoding="utf-8") as f:
        f.write("ĐỒ THỊ TỔNG HỢP \n\n")
        f.write(f"Loại: {'CÓ HƯỚNG' if directed else 'VÔ HƯỚNG'}\n")
        f.write(f"Số đỉnh: {len(adj)}\n")
        f.write("Danh sách đỉnh: " +
                " ".join(str(u) for u in sorted(adj.keys(), key=str)) + "\n\n")

        if canh_thuong:
            f.write(f"Cạnh thường (BFS/DFS/Euler) – {len(canh_thuong)} cạnh:\n")
            for u, v in canh_thuong:
                f.write(f"  {u} {v}\n")
            f.write("\n")

        if canh_trong_so:
            f.write(f"Cạnh có trọng số (Dijkstra/Prim/Kruskal) – {len(canh_trong_so)} cạnh:\n")
            for u, v, w in canh_trong_so:
                f.write(f"  {u} {v} {w}\n")
            f.write("\n")

        if canh_suc_chua:
            f.write(f"Cạnh có sức chứa (Ford-Fulkerson) – {len(canh_suc_chua)} cạnh:\n")
            for u, v, cap_uv, cap_vu in canh_suc_chua:
                f.write(f"  {u}→{v} sức_chứa={cap_uv}   (ngược {v}→{u}={cap_vu})\n")
            f.write("\n")

    print(f" Đã lưu đồ thị vào file '{ten_file}'\n")


 # PHẦN 1: Vẽ đồ thị
def ve_do_thi(G, title="Đồ thị"):
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(G, pos, with_labels=True,
            node_color='lightblue',
            node_size=800,
            font_size=10,
            font_weight='bold',
            edge_color='gray')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.axis('off')
    plt.show()


# PHẦN 3: Đường đi ngắn nhất
def tim_duong_ngan_nhat(G, start, goal):
    try:
        path = nx.shortest_path(G, start, goal, weight='weight')
        length = nx.shortest_path_length(G, start, goal, weight='weight')

        print(f" Đường đi ngắn nhất từ {start} → {goal}:")
        print(path)
        print(f"Độ dài: {length}")
        return path
    except:
        print(" Không tìm thấy đường đi!")
        return None


#  PHẦN 7.2: Kruskal
def kruskal(G):
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

    print("\n Cây khung nhỏ nhất (Kruskal):")
    for u, v, data in mst.edges(data=True):
        print(f"{u} -- {v}   (trọng số: {data.get('weight', 1)})")

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(G, pos, with_labels=True, node_color='lightgray',
            edge_color='lightgray', alpha=0.3)

    nx.draw(mst, pos, with_labels=True, node_color='lightblue',
            edge_color='red', width=3, font_weight='bold')

    edge_labels = nx.get_edge_attributes(mst, 'weight')
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels)

    plt.title("Cây khung nhỏ nhất - Kruskal")
    plt.axis('off')
    plt.show()

    return mst


def _xay_do_thi_nx():
    G = nx.Graph()
    for u in adj:
        for item in adj[u]:
            if isinstance(item, tuple):
                w, v = item
                G.add_edge(u, v, weight=w)
            else:
                G.add_edge(u, v)
    return G


def in_menu():
    print("   1. Thêm đỉnh")
    print("   2. Thêm cạnh thường          (BFS / DFS / Euler)")
    print("   3. Thêm cạnh có trọng số     (Dijkstra / Prim / Kruskal)")
    print("   4. Thêm cạnh có sức chứa     (Ford-Fulkerson)")
    print("   5. Duyệt BFS")
    print("   6. Duyệt DFS")
    print("   7. Ford-Fulkerson")
    print("   8. Chuyển đổi biểu diễn (ma trận kề / danh sách kề / danh sách cạnh)")
    print("   9. Kiểm tra đồ thị 2 phía")
    print("  10. Prim       (cây khung nhỏ nhất)")
    print("  11. Fleury     (đường đi / chu trình Euler)")
    print("  12. Hierholzer (chu trình Euler)")
    print("  13. Lưu đồ thị ra file .txt")
    print("  14. Xóa đồ thị (reset)")
    print("  15. Vẽ đồ thị")
    print("  16. Tìm đường đi ngắn nhất (networkx)")
    print("  17. Kruskal    (cây khung nhỏ nhất)")
    print("   0. Thoát")

def main():
    global directed

    print(" Chọn loại đồ thị:")
    print("   1. Vô hướng (đường 2 chiều)")
    print("   2. Có hướng  (đường 1 chiều)")
    loai = input(" Chọn (1/2): ").strip()
    directed = (loai == "2")
    print("\n Đã tạo đồ thị", "CÓ HƯỚNG" if directed else "VÔ HƯỚNG")

    while True:
        in_menu()
        lua_chon = input(" Chọn: ").strip()

        if lua_chon == "1":
            try:
                k = int(input(" Số đỉnh muốn thêm: "))
                for i in range(k):
                    u = input(f"   Nhập tên đỉnh thứ {i+1}: ").strip()
                    them_dinh(u)
            except ValueError:
                print(" Lỗi: vui lòng nhập số nguyên hợp lệ!")

        elif lua_chon == "2":
            try:
                k = int(input(" Số cạnh muốn thêm: "))
                for i in range(k):
                    parts = input(f"   Cạnh thứ {i+1} (u v): ").split()
                    if len(parts) < 2:
                        print(" Lỗi: cần nhập đúng định dạng 'u v'")
                        continue
                    them_canh(parts[0], parts[1])
            except (ValueError, IndexError):
                print(" Lỗi: nhập sai định dạng!")

        elif lua_chon == "3":
            try:
                k = int(input(" Số cạnh muốn thêm: "))
                for i in range(k):
                    parts = input(f"   Cạnh thứ {i+1} (u v trọng_số): ").split()
                    if len(parts) != 3:
                        print(" Lỗi: cần nhập đúng định dạng 'u v trọng_số'")
                        continue
                    them_canh_trong_so(parts[0], parts[1], int(parts[2]))
            except ValueError:
                print(" Lỗi: trọng số phải là số nguyên!")

        elif lua_chon == "4":
            try:
                k = int(input(" Số cạnh muốn thêm: "))
                for i in range(k):
                    parts = input(f"   Cạnh thứ {i+1} (u v sức_chứa): ").split()
                    if len(parts) != 3:
                        print(" Lỗi: cần nhập đúng định dạng 'u v sức_chứa'")
                        continue
                    them_canh_suc_chua(parts[0], parts[1], int(parts[2]))
            except ValueError:
                print(" Lỗi: sức chứa phải là số nguyên!")

        
        elif lua_chon == "5":
            s = input(" Nhập đỉnh bắt đầu BFS: ").strip()
            BFS(s)

        elif lua_chon == "6":
            s = input(" Nhập đỉnh bắt đầu DFS: ").strip()
            DFS(s)

       
        elif lua_chon == "7":
            s = input(" Nhập đỉnh nguồn (source): ").strip()
            t = input(" Nhập đỉnh đích   (sink):   ").strip()
            ford_fulkerson(s, t)

        elif lua_chon == "8":
            chuyen_doi_bieu_dien()

        elif lua_chon == "9":
            kiem_tra_2_phia()

        elif lua_chon == "10":
            if not adj:
                print(" Đồ thị đang trống!")
            else:
                s = input(" Nhập đỉnh bắt đầu Prim: ").strip()
                prim(s)
        elif lua_chon == "11":
            fleury()

        elif lua_chon == "12":
            hierholzer()

        elif lua_chon == "13":
            luu_do_thi()

        elif lua_chon == "14":
            adj.clear()
            capacity.clear()
            print(" Đã xóa toàn bộ đồ thị!\n")

        elif lua_chon == "15":
            if not adj:
                print(" Đồ thị đang trống!")
            else:
                G = _xay_do_thi_nx()
                ve_do_thi(G, "Đồ thị gốc")

        elif lua_chon == "16":
            if not adj:
                print(" Đồ thị đang trống!")
            else:
                s = input(" Nhập đỉnh bắt đầu: ").strip()
                t = input(" Nhập đỉnh đích: ").strip()
                try:
                    s = int(s)
                except ValueError:
                    pass
                try:
                    t = int(t)
                except ValueError:
                    pass
                G = _xay_do_thi_nx()
                tim_duong_ngan_nhat(G, s, t)

        elif lua_chon == "17":
            if not adj:
                print(" Đồ thị đang trống!")
            else:
                G = _xay_do_thi_nx()
                kruskal(G)

        elif lua_chon == "0":
            print("\n Kết thúc chương trình.\n")
            break

        else:
            print(" Lựa chọn không hợp lệ, vui lòng thử lại!")


if __name__ == "__main__":
    main()
