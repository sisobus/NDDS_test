#include <cstdio>
#include <set>
#include <string>
#include <cassert>
#include <cstring>
#include <algorithm>
#include <map>
#include <vector>
#include <sys/stat.h>
using namespace std;
struct TransformedSpacePoint {
    string originalSequence;
    vector<int> coordinate;
    TransformedSpacePoint(){}
    TransformedSpacePoint(string _originalSequence,int _dimension) {
        originalSequence = _originalSequence;
        coordinate.resize(_dimension,0);
    }
};
vector<string> getDataInInputFile(const string& fileName) {
    vector<string> ret;
    FILE *fp = fopen(fileName.c_str(),"r");
    assert(fp!=NULL);
    char s[1024];

    while ( fgets(s,1024,fp) != NULL ) {
        while ( s[strlen(s)-1] == '\n' || s[strlen(s)-1] == '\r' ) 
            s[strlen(s)-1] = 0;
        ret.push_back(string(s));
    }
    fclose(fp);
    return ret;
}
inline bool isFileExists(const string& fileName) {
    struct stat buffer;
    return (stat(fileName.c_str(),&buffer) == 0);
}
inline int getDistance(string& s1,string& s2) {
    assert(s1.length()==s2.length());
    int ret = 0;
    for ( int i = 0 ; i < (int)s1.length() ; i++ ) 
        ret += (s1[i] != s2[i]);
    return ret;
}
vector<TransformedSpacePoint> getTransformedSpacePoint(vector<string>& data,vector<string>& vantagePoints) {
    assert(!vantagePoints.empty());
    vector<TransformedSpacePoint> ret;
    for ( int i = 0 ; i < (int)data.size() ; i++ ) {
        TransformedSpacePoint cur(data[i],(int)vantagePoints.size());
        for ( int j = 0 ; j < (int)vantagePoints.size() ; j++ ) {
            int dist = getDistance(data[i],vantagePoints[j]);
            cur.coordinate[j] = dist;
        }
        ret.push_back(cur);
    }
    return ret;
}
void printTransformedSpacePoint (TransformedSpacePoint& tData) {
    printf("[%s] : ",tData.originalSequence.c_str());
    for ( int j = 0 ; j < (int)tData.coordinate.size() ; j++ ) 
        printf("%d ",tData.coordinate[j]);
    puts("");
}
void printTransformedSpacePoints(vector<TransformedSpacePoint>& tData) {
    for ( int i = 0 ; i < (int)tData.size() ; i++ ) {
        printTransformedSpacePoint(tData[i]);
    }
}
int main(int argc,char *argv[]) {
    assert(argc==2);
    string dataFileName = string(argv[1]);
    assert(isFileExists(dataFileName));

    vector<string> data = getDataInInputFile(dataFileName);
    vector<string> vantagePoints;
    vantagePoints.push_back("AGTC");
    vantagePoints.push_back("CTGG");
    vector<TransformedSpacePoint> transformedSpaceData = getTransformedSpacePoint(data,vantagePoints);
    printTransformedSpacePoints(transformedSpaceData);
    puts("");

    // CTTC 2,2
    for ( int i = 0 ; i < (int)transformedSpaceData.size() ; i++ ) {
        string test = "CTTC";
        if ( getDistance(transformedSpaceData[i].originalSequence,test) == 1 ) 
            printTransformedSpacePoint(transformedSpaceData[i]);
    }
    return 0;
}
