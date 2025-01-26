from src import code_dom
import re

casing_types = [
    "snake_case",
    "SHOUT_CASE",
    "PascalCase",
    "camelCase"
]


# This modifier renames all DOM elements of a certain type following the given casing type
def apply(dom_root, casing_styles):
    if "types" in casing_styles:
        for element in dom_root.list_all_children_of_type(code_dom.DOMClassStructUnion):
            element.name = change_casing(element.name, casing_styles["types"])
        for element in dom_root.list_all_children_of_type(code_dom.DOMTypedef):
            element.name = change_casing(element.name, casing_styles["types"])
        for element in dom_root.list_all_children_of_type(code_dom.DOMType):
            for token in element.tokens:
                if token.type == "THING" and token.value not in ("int", "char", "bool", "void", "float", "double", "short", "size_t", "va_list", "long"):
                    token.value = change_casing(token.value, casing_styles["types"])
    if "fields" in casing_styles:
        for element in dom_root.list_all_children_of_type(code_dom.DOMFieldDeclaration):
            for i, name in enumerate(element.names):
                element.names[i] = change_casing(name, casing_styles["fields"])
    if "enums" in casing_styles:
        for element in dom_root.list_all_children_of_type(code_dom.DOMEnum):
            element.name = change_casing(element.name, casing_styles["enums"])
    if "functions" in casing_styles:
        for element in dom_root.list_all_children_of_type(code_dom.DOMFunctionDeclaration):
            element.name = change_casing(element.name, casing_styles["functions"])
        for element in dom_root.list_all_children_of_type(code_dom.DOMFunctionArgument):
            element.name = change_casing(element.name, casing_styles["functions"])
    if "macros" in casing_styles:
        for element in dom_root.list_all_children_of_type(code_dom.DOMDefine):
            element.name = change_casing(element.name, casing_styles["macros"])


def change_casing(element_name, casing_type):
    if not element_name:
        return element_name

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
        pascal_case = re.sub(r"([A-z]+?)(_|$)", lambda m: m[1].title() + m[2], underscore_words)
        pascal_case = re.sub(r"_(.)", r"\1", pascal_case)
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
