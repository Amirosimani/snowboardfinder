import logging
import pandas as pd
from scipy.spatial.distance import squareform, pdist

logging.basicConfig(format='%(asctime)s %(levelname)s %(process)d --- %(name)s %(funcName)20s() : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class Similarity:
    logger = logging.getLogger('Similarity')

    def __init__(self):

        self.sel_cols = ['ratings.Riding Style', 'ratings.Riding Level', 'ratings.Shape', 'ratings.Camber Profile',
                         'ratings.Stance', 'ratings.Approx. Weight',
                         'ratings.Powder', 'ratings.Turning', 'ratings.Carving', 'ratings.Speed', 'ratings.Uneven',
                         'ratings.Switch', 'ratings.Jumps', 'ratings.Jibbing', 'ratings.Pipe',
                         #'ratings.On', 'ratings.Turn', 'ratings.Skidded', , 'ratings.Edge'
                         'ratings.Flex', 'ratings.Buttering']
# TODO: scraper has a bug for 4 columns

        self.meta_cols = ['id',
                          'meta_data.name',
                          'meta_data.gender',
                          'meta_data.url',
                          'meta_data.price',
                          'meta_data.image_url'
                          ]

    def calculate_similarity(self, file, topn=10, similarity_algo='jaccard'):
        """

        Args:
            file: input json file downloaded from S3 raw bucket
            topn: find the most similar n items
            similarity_algo: default is jaccard

        Returns:

        """
        # convert json to dataframe
        df_input = self.__prepare_data(file)

        # encode categorical variables used to calcualte disntance
        df_train = pd.get_dummies(df_input[self.sel_cols], columns=self.sel_cols)
        df_distance = self.__distance_function(df_train, similarity_algo)

        # add top n closest item to each row in dataframe
        sim_list = []
        for idx, row in df_distance.iterrows():
            target = df_distance.iloc[:, idx].nsmallest(topn + 1)
            topn_values = target[target != 0].tolist()
            topn_index = target[target != 0].index
            topn_id = df_input['id'][topn_index].tolist()
            sim_dict = dict(zip(topn_id, topn_values))
            sim_list.append(sim_dict)

        df_input['similar_boards'] = sim_list

        return df_input

    @staticmethod
    def __prepare_data(file: list):
        """
        load json file from S3 and convert to dataframe
        Args:
            file: input json file downloaded from S3 raw bucket

        Returns:

        """
        df = pd.json_normalize(file)
        return df

    @staticmethod
    def __distance_function(df, similarity_algo):
        """
        main function to calculate similarity among all the items in the dataframe
        Args:
            df:
            similarity_algo: default is jaccard

        Returns:

        """
        dists = pdist(df, similarity_algo)
        return pd.DataFrame(squareform(dists))



if __name__ == "__main__":

    sim = Similarity()
    df = sim.calculate_similarity('../../data/scraped/men_boards_20220114.json')
    print(df.head())