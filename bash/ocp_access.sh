# A function to download data using named arguments

ocp_get_data () {

    while [ $# -gt 0 ]; do
        case "$1" in
            --server=*)
                server="${1#*=}"
                ;;
            --token=*)
                token="${1#*=}"
                ;;
            --format=*)
                format="${1#*=}"
                ;;
            --x=*)
                x="${1#*=}"
                ;;
            --y=*)
                y="${1#*=}"
                ;;
            --z=*)
                z="${1#*=}"
                ;;
            --zoom=*)
                zoom="${1#*=}"
                ;;
            --help)
                printf "Usage:\n"
                printf "\tocp_get_data --server='servername.com' --token='token00' . . .\n"
                printf "\nFlags:\n"
                printf "\t--server\tServer name (with protocol, http[s])\n"
                printf "\t--token\t\tToken\n"
                printf "\t--zoom\t\tZoom level (0-6)\n"
                printf "\t--x\t\tComma-separated range, e.g. '100,500'\n"
                printf "\t--y\t\tComma-separated range, e.g. '100,500'\n"
                printf "\t--z\t\tComma-separated range, e.g. '100,500'\n"
                ;;
        esac
        shift
    done

    @z_range = split(/,/, $z);

    if [ $z_range[1] -gt $z_range[0] + 16 ]; then
        # download in 16-slice iterations
    else
        curl "${server}/${token}/${format}/${zoom}/${x}/${y}/${z}/" -o "${server}-${token}-${format}-${zoom}-${x}-${y}-${z}.hdf5"
    fi
}
