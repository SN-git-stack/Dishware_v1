"""
This module serves as the interface between a future Web Framework (FastAPI/Flask)
and the underlying AI generation scripts.

It enables "One-Line" calls to run the agents.
"""
import generate_cr
import generate_functional_spec
import generate_director_brief
import evaluate

def web_create_cr(input_text: str):
    """
    Handler to create a new CR from a text blob.
    """
    return generate_cr.handle_web_request(input_text)

def web_generate_spec(cr_filename: str):
    """
    Handler to generate a functional spec from a CR file path.
    Example: web_generate_spec("change_requests/my_cr/my_cr.md")
    """
    # Assuming generate_functional_spec has a similar return structure 
    # (We might need to refactor it to return dicts like generate_cr did)
    try:
        generate_functional_spec.generate_functional_spec(cr_filename)
        return {"success": True, "message": "Spec Generation Started/Completed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def web_generate_brief(cr_filename: str):
    """
    Handler to generate a Director's Brief.
    """
    try:
        generate_director_brief.generate_director_brief(cr_filename)
        return {"success": True, "message": "Brief Generated"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def web_evaluate_cr(cr_filename: str):
    """
    Handler to run the full evaluation.
    """
    try:
        evaluate.evaluate_cr(cr_filename)
        return {"success": True, "message": "Evaluation Complete"}
    except Exception as e:
        return {"success": False, "error": str(e)}
