def create_histogram(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    import logging
    import json
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')
    logging.info('inside histogram')
    import matplotlib.pyplot as plt

    request_json = json.loads(request.get_json())
    if 'url' in request_json:
        values = request_json['url']
        logging.info("get url")
        x = []
        words = 0
        lines = 0
        for k in values.keys():
            v = values[k]
            for i in range(v):
                x.append(int(k))
                words = words + int(k)
            lines = lines + v
        print("number of words:", words)
        print("number of lines: ", lines)
        plt.hist(x, density=False, bins=100)
        plt.ylabel('count')
        plt.xlabel('length of sentences');
        import io
        import base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        img = image_base64
        # """<img src="%s"></img>""" % imgStr
        return img
    else:
        return "error"