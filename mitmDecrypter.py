from mitmproxy.io import FlowReader

def process_flow(flow):
    # Initialize an empty string to hold the formatted data
    formatted_data = ""

    # Check if the flow is an HTTP flow
    if hasattr(flow, 'request'):
        # Format the request data
        formatted_data += f"Request URL: {flow.request.url}\n"
        formatted_data += f"Request Method: {flow.request.method}\n"
        formatted_data += f"Request Headers: {flow.request.headers}\n\n"

        # Format the response data if it exists
        if hasattr(flow, 'response'):
            formatted_data += f"Response Status Code: {flow.response.status_code}\n"
            formatted_data += f"Response Headers: {flow.response.headers}\n"
            formatted_data += f"Response Content: {flow.response.get_text()}\n"
            formatted_data += "----------------------------------------------------------\n\n"

    return formatted_data

def main():
    input_file = 'comlightintheboxandroid.mitm'  # Replace with your .mitm file path
    output_file = 'comlightintheboxandroid.txt'  # The file where you want to save the formatted data

    with open(input_file, 'rb') as f_in, open(output_file, 'w') as f_out:
        reader = FlowReader(f_in)
        for flow in reader.stream():
            formatted_data = process_flow(flow)
            f_out.write(formatted_data)

if __name__ == "__main__":
    main()
