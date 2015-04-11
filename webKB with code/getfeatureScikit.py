from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

# X_train_counts = count_vect.fit_transform('/Users/ChunyueDu/Dropbox/CMU/Courses/2015 Spring/10-601B Machine Learning/Project/gitHub/classifier/webKB with code/newWebkbFile/course/cornell/http:^^cs.cornell.edu^Info^Courses^Current^CS415^CS414.html')
X_train_counts.shape