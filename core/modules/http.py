"""
Module for including functions of HTTP related operations of picocell module.

HTTP Result Codes
------------------------------------------
0 --> Operation successful
701 --> HTTP(S) unknown error
702 --> HTTP(S) timeout
703 --> HTTP(S) busy
704 --> HTTP(S) UART busy
705 --> HTTP(S) no GET/POST/PUT requests
706 --> HTTP(S) network busy
707 --> HTTP(S) network open failed
708 --> HTTP(S) network no configuration
709 --> HTTP(S) network deactivated
710 --> HTTP(S) network error
711 --> HTTP(S) URL error
712 --> HTTP(S) empty URL
713 --> HTTP(S) IP address error
714 --> HTTP(S) DNS error
715 --> HTTP(S) socket create error
716 --> HTTP(S) socket connect error
717 --> HTTP(S) socket read error
718 --> HTTP(S) socket write error
719 --> HTTP(S) socket closed
720 --> HTTP(S) data encode error
721 --> HTTP(S) data decode error
722 --> HTTP(S) read timeout
723 --> HTTP(S) response failed
724 --> Incoming call busy
725 --> Voice call busy
726 --> Input timeout
727 --> Wait data timeout
728 --> Wait HTTP(S) response timeout
729 --> Memory allocation failed
730 --> Invalid parameter
------------------------------------------

HTTP Server Response Codes
---------------------------
200 OK
403 Forbidden
404 Not found
409 Conflict
411 Length required
500 Internal server error
---------------------------
"""

from core.utils.status import Status
from core.utils.helpers import get_parameter

class HTTP:
    """
    Class for including functions of HTTP related operations of picocell module.
    """

    def __init__(self, atcom):
        """
        Initialization of the class.
        """
        self.atcom = atcom

    def set_context_id(self, http_context_id=1):
        """
        Function for setting modem HTTP context id

        Parameters
        ----------
        http_context_id : int
            HTTP context identifier (default=1)(1-16)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPCFG="contextid",{http_context_id}'
        return self.atcom.send_at_comm(command,"OK")

    def set_request_header_status(self, status=0):
        """
        Function for setting modem HTTP request headers status

        Parameters
        ----------
        status : int
            Status of the command.
                0 --> Disable
                1 --> Enable

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPCFG="requestheader",{status}'
        return self.atcom.send_at_comm(command,"OK")

    def set_response_header_status(self, status=0):
        """
        Function for setting modem HTTP response headers status

        Parameters
        ----------
        status : int
            Status of the command.
                0 --> Disable
                1 --> Enable

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPCFG="responseheader",{status}'
        return self.atcom.send_at_comm(command,"OK")

    def set_ssl_context_id(self, id=1):
        """
        Function for setting modem HTTP SSL context id

        Parameters
        ----------
        id : int
            SSL context identifier (default=1)(0-5)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPCFG="sslctxid",{id}'
        return self.atcom.send_at_comm(command,"OK")

    def set_content_type(self, content_type=0):
        """
        Function for setting modem HTTP content type

        Parameters
        ----------
        content_type : str
            Content type (default=0)
                0 --> application/x-www-form-urlencoded
                1 --> text/plain
                2 --> application/octet-stream
                3 --> multipart/form-data
                4 --> application/json
                5 --> image/jpeg

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPCFG="contenttype",{content_type}'
        return self.atcom.send_at_comm(command,"OK")

    def set_auth(self, username=None, password=None):
        """
        Function for setting modem HTTP auth

        Parameters
        ----------
        username : str
            Username (default="")
        password : str
            Password (default="")

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """

        if username:
            username = get_parameter(["https", "username"])

        if password:
            password = get_parameter(["https", "password"])

        if username and password:
            command = f'AT+QHTTPCFG="auth","{username}:{password}"'
            return self.atcom.send_at_comm(command,"OK")
        return {
            "response": "Missing arguments : username and password",
            "status": Status.ERROR
            }

    def set_custom_header(self, header=None):
        """
        Function for setting modem HTTP custom header

        Parameters
        ----------
        header : str
            Custom header (default="")

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        if header:
            command = f'AT+QHTTPCFG="customheader","{header}"'
            return self.atcom.send_at_comm(command,"OK")
        return {"response": "Missing arguments : header", "status": Status.ERROR}

    def set_server_url(self, url=None ,timeout=5):
        """
        Function for setting modem HTTP server URL.
        This command sets the URL of an HTTP(S) Server. The URL must begin with “http://” or
        “https://”, which indicates that an HTTP or HTTPS server will be accessed.

        Parameters
        ----------
        url : str
            Server URL (default="")

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        if url is None:
            url = get_parameter(["https","server"])

        if url:
            len_url = len(url)
            command = f'AT+QHTTPURL={len_url},{timeout}'
            result = self.atcom.send_at_comm(command,"CONNECT")

            if result["status"] == Status.SUCCESS:
                self.atcom.send_at_comm(url, line_end=False) # send url
            return result
        return {"response": "Missing arguments : url", "status": Status.ERROR}

    def get(self, data="", header_mode=0, input_timeout=5, timeout=60):
        """
        Function for sending HTTP GET request

        Parameters
        ----------
        data : str
            The full header for the GET request if header_mode is set.
        header_mode : int
            Customization of HTTP(S) request header)(default=0)
                0 --> Disable
                1 --> Enable
        input_timeout : int
            Input timeout (default=5)
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.
            status : int
                Status of the command.
        """
        # Set the request header config.
        result = self.set_request_header_status(status=header_mode)
        if result["status"] == Status.SUCCESS:
            if header_mode == 1:
                # Send a GET request to the modem.
                command = f'AT+QHTTPGET={timeout},{len(data)},{input_timeout}'
                result =  self.atcom.send_at_comm(command, "CONNECT", timeout=60)
                if result["status"] == Status.SUCCESS:
                    # Send the request header.
                    return self.atcom.send_at_comm(data, "OK", line_end=False)
            else:
                # Send a GET request without header.
                command = f'AT+QHTTPGET={timeout}'
                return self.atcom.send_at_comm(command,"OK")

        # Return the result of request header if there is no SUCCESS.
        return result

    def post(self, data, header_mode=0, input_timeout=5, timeout=60):
        """
        Function for sending HTTP POST request

        Parameters
        ----------
        data : str
            Data to send (default="")
        header_mode : int
            Customization of HTTP(S) request header)(default=0)
                0 --> Only the HTTP(S) POST body should be inputted via a UART/USB port.
                1 --> Both the HTTP(S) POST header and body should be inputted via a UART/USB port.
        input_timeout : int
            Input timeout (default=5)
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.

            status : int
                Status of the command.
        """
        # Set the request header config.
        result = self.set_request_header_status(status=header_mode)
        if result["status"] == Status.SUCCESS:
            # Send a POST request to the modem.
            command = f'AT+QHTTPPOST={len(data)},{input_timeout},{timeout}'
            result =  self.atcom.send_at_comm(command,"CONNECT", timeout=timeout)
            if result["status"] == Status.SUCCESS:
                # Send the request (header and) body.
                result = self.atcom.send_at_comm(data, "OK", line_end=False)
        return result

    def post_from_file(self, file_path, header_mode=0, timeout=60):
        """
        Function for sending HTTP POST file

        Parameters
        ----------
        file_path : str
            File path to send
        header_mode : int
            Customization of HTTP(S) request header)(default=0)
                0 --> The file in a file system will be the HTTP(S) POST body only.
                1 --> The file in a file system will be the HTTP(S) POST header and body.
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.
            status : int
                Status of the command.
        """
        if header_mode == 1:
            return {"response": "Not implemented yet!", "status": Status.ERROR}

        command = f'QHTTPPOSTFILE={file_path},{timeout}'
        return self.atcom.send_at_comm(command,"OK")

    def put(self, data, header_mode=0, input_timeout=5, timeout=60):
        """
        Function for sending HTTP PUT request

        Parameters
        ----------
        data : str
            Data to send
        header_mode : int
            Customization of HTTP(S) request header)(default=0)
                0 --> Only the HTTP(S) PUT body should be inputted via a UART/USB port.
                1 --> Both the HTTP(S) PUT header and body should be inputted via a UART/USB port.
        input_timeout : int
            Input timeout (default=5)
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.
            status : int
                Status of the command.
        """
        # Set the request header config.
        result = self.set_request_header_status(status=header_mode)
        if result["status"] == Status.SUCCESS:
            # Send a PUT request to the modem.
            command = f'AT+QHTTPPUT={len(data)},{input_timeout},{timeout}'
            result = self.atcom.send_at_comm(command,"CONNECT")
            if result["status"] == Status.SUCCESS:
                # Send the request (header and) body.
                result = self.atcom.send_at_comm(data, "OK", line_end=False)
        return result

    def put_from_file(self, file_path, file_type=0, header_mode=0, timeout=60):
        """
        Function for sending HTTP PUT file

        Parameters
        ----------
        file_path : str
            File path to send
        file_type : int
            File type File information to be sent. This parameter can only be omitted 
            when <file_type>=0.(default=0)
                0 -->
                    * If <request_header>=0, it indicates request body
                    * If <request_header>=1, it indicates both request header and body
                1 --> Request header (<request_header> must be set to 1)
                2 --> Request body (<request_header> must be set to 1)
        header_mode : int
            Customization of HTTP(S) request header)(default=0)
                0 --> Disable
                1 --> Enable
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.
            status : int
                Status of the command.
        """
        if header_mode == 1:
            return {"response": "Not implemented yet!", "status": Status.ERROR}

        command = f'AT+QHTTPPUTFILE={file_path},{timeout},{file_type}'
        return self.atcom.send_at_comm(command,"OK")

    def read_response(self, timeout=60):
        """
        Function for retrieving the HTTP(S) response from an HTTP(S) server via the UART/USB port,
        after HTTP(S) GET/POST/PUT requests are sent.

        Parameters
        ----------
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPREAD={timeout}'
        return self.atcom.send_at_comm(command,"OK", timeout=timeout)

    def read_response_to_file(self, file_path, timeout=60):
        """
        Function for storing the HTTP(S) response from an HTTP(S) server to a specified file,
        after HTTP(S) GET/POST/PUT requests are sent, thus allowing users to retrieve the response
        information from the file.

        Parameters
        ----------
        file_path : str
            File path to save
        timeout : int
            Timeout (default=60)

        Returns
        -------
        (response, status) : tuple
            response : str (<result>[,<httprspcode>[,<content_length>]])
                Response from the command
                    - result : int
                        Result Code of HTTP(S)
                    - httprspcode : int
                        HTTP(S) response code
                    - content_length : int
                        Length of HTTP(S) response body.
            status : int
                Status of the command.
        """
        command = f'AT+QHTTPREADFILE={file_path},{timeout}'
        return self.atcom.send_at_comm(command,"OK")
