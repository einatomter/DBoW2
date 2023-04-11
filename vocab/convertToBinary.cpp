#include "DBoW2.h" // defines OrbVocabulary and OrbDatabase


// #include"FORB.h"
// #include"TemplatedVocabulary.h"

typedef DBoW2::TemplatedVocabulary<DBoW2::FORB::TDescriptor, DBoW2::FORB>
  ORBVocabulary;

int main()
{
    std::cout << "running convertToBinary.cpp" << std::endl;
    ORBVocabulary voc("aqualoc.yml.gz");
    voc.saveToBinaryFile("aqualoc.txt.bin");
    std::cout << "done" << std::endl;
    return 0;
}