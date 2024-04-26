library(car)
library(olsrr)

df <- read.csv("../data/processed/papers_to_study_expanded.csv")
dim(df)

# dff <- df[!(df$doi == '10.1111/j.1460-2466.1977.tb02133.x'),]

sapply(list(df$first_author_country), unique)
df$Year.Distance.from.2022 = abs(df$year - 2022)
df$gscholar_citation_log10 <- log10(df$gscholar_citation + 0.1)
var_cols <- c(1, 11, 16:17, 20:33, 35:36)
data <- df[, var_cols]

## Checking outlier

hist(data$gscholar_citation_log10)
data$gscholar_citation_log10_stdized <- scale(
  data$gscholar_citation_log10,
  center = T,
  scale = T
)
data$outlier0 <- ifelse(data$gscholar_citation_log10_stdized > 3.3 | 
                          data$gscholar_citation_log10_stdized < -3.3,
                        1, 0
)
table(data$outlier0)

datanew <- subset(data, outlier0 == 0)
datanew$outlier0 <- NULL
datanew$gscholar_citation_log10_stdized <- NULL


model <- lm(gscholar_citation_log10~., datanew)
summary(model)


## Normality
ols_plot_resid_qq(model)

#Correlation between observed residuals and expected residuals under normality.
ols_test_correlation(model)

ols_plot_resid_hist(model)

## linearity & homoscedasticity 
ols_plot_resid_fit(model)

## collinearity diagnostics
# ols_coll_diag(model)
vif(model)

## all in one
# ols_plot_diagnostics(model)

library(stargazer)
stargazer(model, type = "html", out = "figures/lm.html")

# ## multivariate outliers
# alpha <- 0.5
# cutoff <- (qchisq(p = 1- alpha, df = 3))
# # 
# # character_vars <- lapply(data, class) == "character"
# # character_vars
# # to_factor_col_idx <- c(1:3, 6:9, 11:17)
# # to_factor_col_name <- colnames(data)[to_factor_col_idx]
# # data[to_factor_col_name] <- lapply(data[to_factor_col_name], factor)
# 
# # change categorical to numeric
# # https://stackoverflow.com/a/47922961
# data[] <- data.matrix(data)
# 
# data$mahal1 <- mahalanobis(
#   data[c(1:18)],
#   colMeans(data[c(1:18)]),
#   cov(data[c(1:18)])
# )
# 
# data$outlier1 <- ifelse(data$mahal1>cutoff, 1, 0)
# 
# ## there are many multivariate outliers
# table(data$outlier1)
