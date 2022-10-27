@app.route("/rule", methods=["GET", "POST"])
def rule():
    data = request.get_json(silent=True)
    if data and set(data.keys()).issubset({"ticker", "action", "price"}):
        r = Rule(ticker=data["ticker"], action=data["action"], price=data["price"])
        db.session.add(r)
        db.session.commit()
        return data
    else:
        abort(404)
        return "error"
