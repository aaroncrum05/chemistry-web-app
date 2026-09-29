import csv
from pathlib import Path

from flask import Flask, render_template_string, request

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("matchem.csv")

PAGE = """<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Alloy Chemistry</title>
        <style>
            :root {
                color-scheme: light;
                font-family: "Segoe UI", sans-serif;
                color: #18302f;
                background: #f2f5f1;
            }
            body { margin: 0; }
            header {
                padding: 2rem max(1.25rem, calc((100% - 760px) / 2));
                color: #f8fbf7;
                background: #174d48;
            }
            header h1 { margin: 0; font-size: 1.8rem; }
            main { max-width: 760px; margin: 2rem auto; padding: 0 1.25rem; }
            form { display: grid; gap: 0.6rem; max-width: 420px; }
            label { font-weight: 650; }
            select {
                width: 100%;
                padding: 0.75rem;
                border: 1px solid #9aadaa;
                border-radius: 4px;
                background: white;
                color: inherit;
                font: inherit;
            }
            section { margin-top: 2rem; }
            h2 { margin-bottom: 0.35rem; }
            .meta { margin-top: 0; color: #536563; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { padding: 0.7rem 0.85rem; border-bottom: 1px solid #d9e1dd; text-align: left; }
            th:last-child, td:last-child { text-align: right; }
            th { color: #36514e; background: #e3ebe6; }
            tbody tr:last-child td { border-bottom: 0; }
            @media (max-width: 520px) {
                header { padding-top: 1.5rem; padding-bottom: 1.5rem; }
                main { margin-top: 1.5rem; }
            }
        </style>
    </head>
    <body>
        <header><h1>Alloy Chemistry</h1></header>
        <main>
            <form method="get">
                <label for="alloy">Select an alloy</label>
                <select id="alloy" name="alloy" onchange="this.form.submit()">
                    <option value="">Choose an alloy...</option>
                    {% for alloy in alloys %}
                    <option value="{{ alloy.Alloy }}" {% if selected and selected.Alloy == alloy.Alloy %}selected{% endif %}>{{ alloy.Alloy }}</option>
                    {% endfor %}
                </select>
            </form>
            {% if selected %}
            <section aria-live="polite">
                <h2>{{ selected.Alloy }}</h2>
                <p class="meta">Base element: {{ selected.Base_Element }}{% if selected.Engine_Location %} · Used in {{ selected.Engine_Location }}{% endif %}</p>
                <table>
                    <thead><tr><th>Element</th><th>Composition (%)</th></tr></thead>
                    <tbody>
                        {% for element, amount in chemistry %}
                        <tr><td>{{ element }}</td><td>{{ amount|float|round(2) }}%</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>
            {% endif %}
        </main>
    </body>
</html>
"""


def load_alloys():
    with DATA_FILE.open(newline="", encoding="utf-8-sig") as csv_file:
        return list(csv.DictReader(csv_file))


@app.route("/")
def home():
    alloys = load_alloys()
    selected_name = request.args.get("alloy", "")
    selected = next((alloy for alloy in alloys if alloy["Alloy"] == selected_name), None)
    chemistry = []
    if selected:
        metadata_fields = {"Alloy", "Base_Element", "Engine_Location"}
        chemistry = [
            (element, amount)
            for element, amount in selected.items()
            if element not in metadata_fields and float(amount or 0) != 0
        ]

    return render_template_string(PAGE, alloys=alloys, selected=selected, chemistry=chemistry)

if __name__ == "__main__":
    app.run(debug=True)