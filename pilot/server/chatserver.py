from flask import Flask, request, Response
import json
import os
import sys
import threading
from queue import Queue
from itertools import zip_longest
from transformers import pipeline

# Define the Flask app
app = Flask(__name__)

# Define the path to the knowledge base for each user group
knowledge_bases = {
    'group1': '/path/to/knowledge/base1',
    'group2': '/path/to/knowledge/base2',
    # Add more knowledge bases for other user groups
}

# Define a queue to store the generated content
output_queue = Queue()

# Define a function to generate content using a large language model
def generate_content(model_name, prompt, knowledge_base):
    # Load the language model pipeline
    generator = pipeline('text-generation', model=model_name, device=0)

    # Generate content based on the prompt and the knowledge base
    generated = generator(
        prompt,
        max_length=1000,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.2,
        temperature=0.7,
        padding_text=knowledge_base,
        pad_token_id=generator.tokenizer.eos_token_id,
        return_tensors='pt'
    )

    # Convert the generated content from tensors to strings
    generated_text = [generator.tokenizer.decode(g, skip_special_tokens=True) for g in generated]

    # Add the generated content to the output queue
    output_queue.put(generated_text)

# Define a function to stream the generated content to the client
def generate_output():
    # Set the response headers
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }

    # Start the response with the headers
    yield '\n'.join(f'{k}: {v}' for k, v in headers.items()) + '\n\n'

    # Stream the generated content to the client
    while True:
        try:
            output = output_queue.get(timeout=1)
        except:
            output = []

        if not output:
            continue

        for message in output:
            data = {'message': message}
            yield f'data: {json.dumps(data)}\n\n'

# Define the API endpoint
@app.route('/api/generate', methods=['POST'])
def generate():
    # Get the user group and message from the request
    group = request.form.get('group')
    message = request.form.get('message')

    # Get the path to the knowledge base for the user group
    knowledge_base_path = knowledge_bases.get(group)

    # Check if the knowledge base exists
    if not knowledge_base_path:
        return 'Invalid user group'

    # Read the knowledge base file
    with open(knowledge_base_path, 'r') as f:
        knowledge_base = f.read()

    # Generate content using a separate thread
    model_name = 'gpt2'
    t = threading.Thread(target=generate_content, args=(model_name, message, knowledge_base))
    t.start()

    # Return the generated content in a streaming way
    return Response(generate_output(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)