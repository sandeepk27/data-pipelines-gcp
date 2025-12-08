import argparse
import logging
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

class ParseMessage(beam.DoFn):
    def process(self, element):
        """
        Parses the JSON message from Pub/Sub.
        """
        try:
            row = json.loads(element.decode("utf-8"))
            yield row
        except Exception as e:
            logging.error(f"Error parsing json: {e}")

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_subscription',
        help='Input PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>".')
    parser.add_argument(
        '--output_table',
        help='Output BigQuery table for results')

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    # streaming=True is crucial for streaming pipelines
    pipeline_options.view_as(beam.options.pipeline_options.StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "ReadFromPubSub" >> beam.io.ReadFromPubSub(subscription=known_args.input_subscription)
            | "ParseJSON" >> beam.ParDo(ParseMessage())
            | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                known_args.output_table,
                schema='id:INTEGER, name:STRING, timestamp:TIMESTAMP',
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
