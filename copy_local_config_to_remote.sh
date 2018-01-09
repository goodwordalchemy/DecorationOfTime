for line in $(cat .env)
do
    if [ "$line" != 'export' ]
    then
        heroku config:set $line
    fi
done

