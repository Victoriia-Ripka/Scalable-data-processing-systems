library(sparklyr)
options(sparklyr.log.console = TRUE)
sc <- spark_connect(master = "local[*]", config = list(sparklyr.gateway.port = 8881))
iris_spark <- copy_to(sc, iris, overwrite = TRUE)
iris_spark %>%
  summarise(count = n()) %>%
  collect() %>%
  print()
spark_disconnect(sc)