from flask import Flask, request, jsonify, render_template
import time, random

app = Flask(__name__)

paragraphs = [
    "Technology has transformed the way people live and work. From smartphones to artificial intelligence, innovations have created endless opportunities. Students can now learn online, and businesses can reach global audiences instantly. With these benefits, it is important to also consider digital wellbeing, balance, and responsible usage of technology in daily life.",
    
    "Nature provides everything essential for human survival, including fresh air, water, and food. Forests, rivers, and oceans play a vital role in maintaining ecological balance. Protecting the environment is not only a duty but also a necessity for a healthy future. Small actions like reducing waste and planting trees can create change.",
    
    "Reading is one of the most valuable habits a person can develop. It improves vocabulary, stimulates imagination, and enhances knowledge. Books allow readers to travel through time and space, experiencing different cultures and ideas. In a digital age filled with distractions, dedicating time to reading can build focus and lifelong learning skills.",
    
    "Teamwork is the foundation of success in many fields, including sports, education, and business. When individuals collaborate effectively, they combine skills and knowledge to achieve goals faster. Good communication, trust, and respect are essential in teamwork. A united group can overcome challenges that might seem impossible for individuals working alone.",
    
    "Once upon a time, a farmer lived in a small village with his three sons. They always quarreled with each other, which made the farmer sad. One day, he gave them a bundle of sticks and asked them to break it. Together, they failed, and they finally understood the strength of unity.",
    
    "Riya loved painting, but she lacked confidence in her talent. One day, her teacher encouraged her to participate in a school competition. She worked hard, practiced daily, and finally won the first prize. That victory not only boosted her confidence but also taught her that dedication can turn dreams into reality.",
    
    "Traveling opens the door to new cultures, traditions, and experiences. Walking through busy streets, tasting unique foods, and meeting people from different backgrounds helps us understand the world better. Each journey creates stories and memories that last a lifetime. Exploring new places is not just fun, but also a form of learning.",
    
    "In the middle of the night, the old clock in the hallway struck twelve. The house was silent except for the soft rustle of the wind outside. Suddenly, a loud knock echoed at the door. Arun hesitated, his heart racing, as he slowly stepped forward to see who it was.",
    
    "Discipline is like the bridge between goals and achievements. A student who studies regularly, an athlete who trains daily, and a worker who manages time wisely are more likely to succeed. While talent is important, discipline ensures consistency, and consistency is the secret ingredient that transforms dreams into accomplishments over time.",
    
    "Long ago, there was a clever rabbit who lived in a forest. One day, the lion declared himself king and started troubling other animals. Tired of the lion’s cruelty, the rabbit devised a plan. With his intelligence, he tricked the lion into falling into a deep well, saving the entire forest."
]

current_paragraph = None
start_time = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/paragraph", methods=["GET"])
def get_paragraph():
    global current_paragraph
    if current_paragraph is None:
        current_paragraph = random.choice(paragraphs)
    return jsonify({"paragraph": current_paragraph})

@app.route("/change", methods=["GET"])
def change_paragraph():
    global current_paragraph
    new_para = random.choice([p for p in paragraphs if p != current_paragraph])
    current_paragraph = new_para
    return jsonify({"paragraph": current_paragraph})

@app.route("/start", methods=["GET"])
def start():
    global start_time
    start_time = time.time()  # optional note; main timer is client-side
    return jsonify({"message": "Start typing the given paragraph!"})

@app.route("/finish", methods=["POST"])
def finish():
    global start_time, current_paragraph
    if start_time is None:
        return jsonify({"error": "Test not started"}), 400

    typed_text = request.json.get("text", "")
    end_time = time.time()
    elapsed = end_time - start_time

    word_count = len(typed_text.strip().split()) if typed_text.strip() else 0
    time_in_minutes = elapsed / 60
    wpm = (word_count / time_in_minutes) if time_in_minutes > 0 else 0

    expected_words = current_paragraph.strip().split()
    typed_words = typed_text.strip().split()
    correct = sum(1 for ew, tw in zip(expected_words, typed_words) if ew == tw)
    accuracy = (correct / len(expected_words)) * 100 if expected_words else 0

    start_time = None

    return jsonify({
        "words": word_count,
        "time": round(elapsed, 2),
        "wpm": round(wpm, 2),
        "accuracy": round(accuracy, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
