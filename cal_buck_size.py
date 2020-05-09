import os
from google.cloud import monitoring_v3
buck_nm = '[bucket Name]'
buck_loc = '[bucket Location]'
project_nm = '[project Name]'
client = monitoring_v3.MetricServiceClient()
project_name = client.project_path(project_nm)
interval = monitoring_v3.types.TimeInterval()
now = time.time()
interval.end_time.seconds = int(now)
interval.end_time.nanos = int((now - interval.end_time.seconds) * 10**9)
interval.start_time.seconds = int(now - 3600)
interval.start_time.nanos = interval.end_time.nanos
aggregation = monitoring_v3.types.Aggregation()
aggregation.alignment_period.seconds = 3600  
aggregation.per_series_aligner = (monitoring_v3.enums.Aggregation.Aligner.ALIGN_MEAN)
#Define filter base on resource
filter = 'resource.type = "gcs_bucket" AND resource.labels.bucket_name = \"'+buck_nm+'\" AND resource.labels.location = '+buck_loc+' AND resource.labels.project_id = '+project_nm+' AND metric.type = "storage.googleapis.com/storage/total_bytes"'
results = client.list_time_series(
                    project_name,
                    filter,
                    interval, 
                    monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL,
                    aggregation)
for result in results:
     buck_sz = result.points[0].value.double_value/(1024*1024)
print('Bucket {} size is {}Mb'.format(buck_nm,buck_sz))
