library(dplyr)
library(ggplot2)
library(reshape2)
library(gridExtra)

file_path <- "data/StudentsPerformance.csv" 
data <- read.csv(file_path, stringsAsFactors = FALSE)

colnames(data) <- gsub("\\.", "_", tolower(colnames(data)))  
data <- data %>%
  mutate(
    math_score = as.numeric(math_score),
    reading_score = as.numeric(reading_score),
    writing_score = as.numeric(writing_score)
  )

data <- data %>%
  mutate(
    total_score = math_score + reading_score + writing_score,
    average_score = total_score / 3
  )

p1 <- ggplot(data, aes(x = math_score)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black", alpha = 0.7) +
  labs(title = "Розподіл оцінок з математики", x = "Оцінка з математики", y = "Частота") +
  theme_minimal()

p2 <- ggplot(data, aes(x = reading_score)) +
  geom_histogram(binwidth = 1, fill = "red", color = "black", alpha = 0.7) +
  labs(title = "Розподіл оцінок з читання", x = "Оцінка з читання", y = "Частота") +
  theme_minimal()

p3 <- ggplot(data, aes(x = writing_score)) +
  geom_histogram(binwidth = 1, fill = "green", color = "black", alpha = 0.7) +
  labs(title = "Розподіл оцінок з письма", x = "Оцінка з письма", y = "Частота") +
  theme_minimal()

print(grid.arrange(p1, p2, p3, ncol = 1))

stats <- data %>%
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

print("Статистика оцінок:")
print(stats)

ggplot(data) +
  geom_boxplot(aes(y = math_score, fill = "Math")) +
  geom_boxplot(aes(y = reading_score, fill = "Reading")) +
  geom_boxplot(aes(y = writing_score, fill = "Writing")) +
  scale_fill_manual(values = c("blue", "red", "green")) +
  labs(title = "Boxplot оцінок", y = "Оцінка", x = "Предмет") +
  theme_minimal()

ggplot(data, aes(x = parental_level_of_education, y = average_score, fill = parental_level_of_education)) +
  geom_boxplot() +
  labs(title = "Розподіл середніх оцінок за рівнем освіти батьків", y = "Середня оцінка", x = "Освіта батьків") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  theme_minimal()