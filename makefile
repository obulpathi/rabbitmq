# help message
help:
	/root/tools/runjava.sh com.rabbitmq.examples.PerfTest --help

# Send transient messages without acknowledgement, 1 producer and 1 consumer.
simple:
	/root/tools/runjava.sh com.rabbitmq.examples.PerfTest --queue myqueue --uri amqp://username:password@rabbitmq:5672/vhost

# Similar, but with acknowledgments and confirms.
confirm:
	runjava.sh com.rabbitmq.examples.PerfTest --confirm 1000 --uri amqp://username:password@rabbitmq:5672/vhost

# ...with acknowledgments, confirms and persistence.
persistent:
	/root/tools/runjava.sh com.rabbitmq.examples.PerfTest --confirm 1000 --flag persistent --uri amqp://username:password@rabbitmq:5672/vhost

# Fill a pre-declared queue with 1M transient messages of 1kB each
produce:
	/root/tools/runjava.sh com.rabbitmq.examples.PerfTest -consumers 0 --predeclared --queue myqueue -size 1000 -pmessages 1000000 --uri amqp://username:password@rabbitmq:5672/vhost

# Start 10 consumers from a predeclared queue, and no producers.
consume:
	/root/tools/runjava.sh com.rabbitmq.examples.PerfTest --producers 0 --consumers 10 --predeclared --queue myqueue --uri amqp://username:password@rabbitmq:5672/vhost
