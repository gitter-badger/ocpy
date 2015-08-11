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

    z_lo=`echo $z | cut -d "," -f 1`;
    z_hi=`echo $z | cut -d "," -f 2`;

    if [[ $z_hi -gt $( $z_lo + 16 ) ]]; then
        # download in 16-slice iterations
        i=$z_lo
        while [[ $i -lt $z_hi ]] do
            if [[ $( $i + 16 ) -gt $z_hi ]]; then
                curl -L "${server}/${token}/${format}/${zoom}/${x}/${y}/${i},${z_hi}/" -o "${token}-${format}-${zoom}-${x}-${y}-${i},${z_hi}.hdf5"
            else
                curl -L "${server}/${token}/${format}/${zoom}/${x}/${y}/${i},`expr $i + 16`/" -o "${token}-${format}-${zoom}-${x}-${y}-${i},`expr $i + 16`.hdf5"
            i=`expr $i + 17`
            fi
        done
    else
        curl -L "${server}/${token}/${format}/${zoom}/${x}/${y}/${z}/" -o "${token}-${format}-${zoom}-${x}-${y}-${z}.hdf5"
    fi
}
