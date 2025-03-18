library(sparklyr)
library(dplyr)

sc <- spark_connect(master = "local[*]")
print(sc)

print("Початок завантаження даних")
data_spark <- spark_read_csv(sc, name = "students_performance", 
                             path = "data/StudentsPerformance.csv", 
                             header = TRUE, infer_schema = TRUE)
print("Дані завантажено")

print("Переведення і обробка даних")
data_spark <- data_spark %>%
  rename_with(~ gsub("\\.", "_", tolower(.))) %>%
  mutate(
    math_score = as.double(math_score),
    reading_score = as.double(reading_score),
    writing_score = as.double(writing_score),
    total_score = math_score + reading_score + writing_score,
    average_score = total_score / 3
  )
print("Дані оброблено")

print("Виконання статистичних обчислень")
stats_spark <- data_spark %>%
  summarise(
    math_mean = mean(math_score, na.rm = TRUE),
    reading_mean = mean(reading_score, na.rm = TRUE),
    writing_mean = mean(writing_score, na.rm = TRUE),
    avg_score_mean = mean(average_score, na.rm = TRUE),
    math_max = max(math_score, na.rm = TRUE),
    reading_max = max(reading_score, na.rm = TRUE),
    writing_max = max(writing_score, na.rm = TRUE),
    avg_score_max = max(average_score, na.rm = TRUE),
    math_min = min(math_score, na.rm = TRUE),
    reading_min = min(reading_score, na.rm = TRUE),
    writing_min = min(writing_score, na.rm = TRUE),
    avg_score_min = min(average_score, na.rm = TRUE)
  )
print("Статистику обчислено")

print("Виведення результатів")
stats_spark %>% sdf_collect() %>% print()

hist_data <- sdf_histogram(data_spark, "math_score", bins = 10)
print(hist_data)

spark_disconnect(sc)