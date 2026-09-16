from luckytools import LuckyTools # pip install luckytools

lt = LuckyTools(prefix_name="⌊ Main ⌉ »", prefix_hex="00AAFF", prefix_short="⌊ FM ⌉ »")

def memory_id() -> None:
    lt.print(f"int", color="FF0000")
    num = 100
    num_2 = num

    lt.print(f"num: id {id(num)}\n"
             f"num: id {id(num_2)}\n"
             f"{id(num)} = {id(num_2)}",
             animate=True, color="FFFFFF", white_tag=True, time_show=0.1)

    num += 1

    lt.print(f"num += 1")
    lt.print(f"num: id {id(num)}\n"
             f"num: id {id(num_2)}\n"
             f"{id(num)} != {id(num_2)}",
             animate=True, color="FFFFFF", white_tag=True, time_show=0.1)

    num_2 += 1

    lt.print(f"num_2 += 1")
    lt.print(f"num: id {id(num)}\n"
             f"num: id {id(num_2)}\n"
             f"{id(num)} = {id(num_2)}",
             animate=True, color="FFFFFF", white_tag=True, time_show=0.1)

    lt.print(f"list", color="FF0000")
    lst = [100]
    lst_2 = lst

    lt.print(f"lst: id {id(lst)}\n"
             f"lst: id {id(lst_2)}\n"
             f"{id(lst)} = {id(lst_2)}",
             animate=True, color="FFFFFF", white_tag=True, time_show=0.1)

    lst.append(100)

    lt.print(f"lst: id {id(lst)}\n"
             f"lst: id {id(lst_2)}\n"
             f"{id(lst)} = {id(lst_2)}",
             animate=True, color="FFFFFF", white_tag=True, time_show=0.1)

memory_id()
