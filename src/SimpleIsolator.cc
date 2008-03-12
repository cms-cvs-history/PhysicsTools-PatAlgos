#include "PhysicsTools/PatAlgos/interface/SimpleIsolator.h"
#include <sstream>

using pat::helper::SimpleIsolator;
using pat::helper::BaseIsolator;


SimpleIsolator::SimpleIsolator(const edm::ParameterSet &conf) :
    BaseIsolator(conf)
{
}

void
SimpleIsolator::beginEvent(const edm::Event &event) {
    event.getByLabel(input_, handle_);
}

void
SimpleIsolator::endEvent() {
    handle_.clear();
}

