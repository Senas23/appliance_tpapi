"""
tex_api
    A Python client side utility for using Threat Extraction API calls to an appliance.

    You may either set the global variables below (some or all), or assigning their optional
      arguments when running the utility.  Run  tex_api --help  for the arguments details.
"""

from tex_file_handler import TEX
import os
import argparse


input_directory = "/home/admin/TEX_API/input_files"
output_directory = "/home/admin/TEX_API/tex_response_data"
api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
appliance_ip = "NNN.NNN.NNN.NNN"


def main():
    """
    1. Get the optional arguments (if any): the input-directory, the output-root-directory,
        the api-key, either the appliance-ip or the appliance-FQDN and the SSL-certificate.
        Note: if using an SSL-certificate then must also use the FQDN.
    2. Accordingly set the api-url, and create the output directory.
    3. Go though all input files in the input directory.
        Handling each input file is described in TEX class in tex_file_handler.py:
    """
    global input_directory
    global output_directory
    global appliance_ip
    global api_key
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--input_directory", help="the input files folder to be scanned by TEX")
    parser.add_argument("-od", "--output_directory", help="the output folder with TEX results")
    parser.add_argument("-ak", "--api_key", help="the appliance api key")
    parser.add_argument("-ip", "--appliance_ip", help="the appliance ip address.  If used, then cannot use fqdn")
    parser.add_argument("-fq", "--fqdn", help="the appliance FQDN.  If used, then cannot use ip_address")
    parser.add_argument("-ct", "--cert_file",
                        help="valid SSL certificate file (full path), which matches the appliance FQDN." +
                             "  If used, then must also use fqdn")
    args = parser.parse_args()
    if args.input_directory:
        input_directory = args.input_directory
    print("The input files directory to be scanned by TEX : {}".format(input_directory))
    if not os.path.exists(input_directory):
        print("The input files directory {} does not exist !".format(input_directory))
        return
    if args.output_directory:
        output_directory = args.output_directory
    print("The output directory with TEX results : {}".format(output_directory))
    if not os.path.exists(output_directory):
        print("Pre-processing: creating tex_api output directory {}".format(output_directory))
        try:
            os.mkdir(output_directory)
        except Exception as E1:
            print("could not create tex_api output directory, because: {}".format(E1))
            return
    if args.api_key:
        api_key = args.api_key
    print("The appliance api key : {}".format(api_key))
    if args.appliance_ip:
        appliance_ip = args.appliance_ip
    if args.fqdn:
        if args.appliance_ip:
            print("Cannot use both arguments: appliance_ip and fqdn. Use just one of them. If using cert_file" +
                  "argument then must also use fqdn argument.")
            return
        print("The appliance FQDN : {}".format(args.fqdn))
        url = "https://" + args.fqdn + "/UserCheck/TPAPI"
    else:
        print("The appliance ip address : {}".format(appliance_ip))
        url = "https://" + appliance_ip + "/UserCheck/TPAPI"
    if args.cert_file:
        if not args.fqdn:
            print("Using cert_file argument requires using also fqdn argument.")
            return
        print("The valid certificate file, that should match the appliance FQDN : {}".format(args.cert_file))

    # A loop over the files in the input folder
    print("Begin handling input files by TEX")
    for file_name in os.listdir(input_directory):
        try:
            full_path = os.path.join(input_directory, file_name)
            print("Handling file: {} by TEX".format(file_name))
            tex = TEX(url, api_key, file_name, full_path, output_directory, args.cert_file)
            tex.handle_file()
        except Exception as E:
            print("could not handle file: {} because: {}. Continue to handle next file".format(file_name, E))
            continue


if __name__ == '__main__':
    main()
