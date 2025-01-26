import re

casing_types = [
    "snake_case",
    "SHOUT_CASE",
    "PascalCase",
    "camelCase"
]


# This modifier renames all DOM elements of a certain type following the given casing type
def apply(dom_root, element_types, casing_type):
    for element_type in element_types:
        for element in dom_root.list_all_children_of_type(element_type):
            if hasattr(element, 'name') and element.name is not None:
                element.name = change_casing(element.name, casing_type)
            if hasattr(element, 'names'):
                for i, name in enumerate(element.names):
                    element.names[i] = change_casing(name, casing_type)


def change_casing(element_name, casing_type):
    # Put an underscore between changes from lowercase to uppercase
    underscore_words = re.sub(r"([a-z])([A-Z])", r"\1_\2", element_name)

    if casing_type == "snake_case":
        snake_case = underscore_words.lower()
        # Replace im_gui_whatever with imgui_whatever
        if snake_case.startswith("im_"):
            snake_case = "im" + snake_case.removeprefix("im_")
        if snake_case.startswith("c_im_"):
            snake_case = "cim" + snake_case.removeprefix("c_im_")
        snake_case = snake_case.replace("open_gl", "opengl")
        return snake_case

    elif casing_type == "SHOUT_CASE":
        shout_case = underscore_words.upper()
        # Replace IM_GUI_WHATEVER with IMGUI_WHATEVER
        if shout_case.startswith("IM_"):
            shout_case = "IM" + shout_case.removeprefix("IM_")
        if shout_case.startswith("C_IM_"):
            shout_case = "CIM" + shout_case.removeprefix("C_IM_")
        shout_case = shout_case.replace("OPEN_GL", "OPENGL")
        return shout_case

    elif casing_type == "PascalCase":
        # Don't replace ImGuiWhatever with ImguiWhatever
        # Match all words and make them lowercase with first one capitalized
        pascal_case = re.sub(r"([A-z]+?)(_|$)", lambda m: m[1].title(), underscore_words)
        return pascal_case

    elif casing_type == "camelCase":
        snake_case = underscore_words.lower()
        # Replace imGuiWhatever with imguiWhatever
        if snake_case.startswith("im_"):
            snake_case = "im" + snake_case.removeprefix("im_")
        if snake_case.startswith("c_im_"):
            snake_case = "cim" + snake_case.removeprefix("c_im_")
        snake_case = snake_case.replace("open_gl", "opengl")
        # Match all words and make them lowercase with first one capitalized
        pascal_case = re.sub(r"([A-z]+?)(_|$)", lambda m: m[1].title(), snake_case)
        camel_case = pascal_case[0].lower() + pascal_case[1:]
        return camel_case

    else:
        raise Exception(f"Unknown casing type: {casing_type} (supported: {', '.join(casing_types)})")
