library(dplyr)
library(ggplot2)

file_path <- "data/StudentsPerformance.csv" 
data <- read.csv(file_path, stringsAsFactors = FALSE)
head(data)

colnames(data) <- gsub("\\.", "_", tolower(colnames(data)))  

data <- data %>%
  mutate(
    math_score = as.numeric(math_score),
    reading_score = as.numeric(reading_score),
    writing_score = as.numeric(writing_score)
  )

summary_data <- data %>%
  group_by(race_ethnicity) %>%  
  summarise(
    avg_math = mean(math_score, na.rm = TRUE),
    avg_reading = mean(reading_score, na.rm = TRUE),
    avg_writing = mean(writing_score, na.rm = TRUE)
  )

print(summary_data)

plot <- ggplot(summary_data, aes(x = race_ethnicity)) +
  geom_bar(aes(y = avg_math, fill = "Math"), stat = "identity", position = "dodge") +
  geom_bar(aes(y = avg_reading, fill = "Reading"), stat = "identity", position = "dodge") +
  geom_bar(aes(y = avg_writing, fill = "Writing"), stat = "identity", position = "dodge") +
  scale_fill_manual(values = c("blue", "red", "green")) +
  labs(title = "Середні бали з предметів за расовими групами", y = "Середній бал", x = "Група") +
  theme_minimal()

print(plot) 