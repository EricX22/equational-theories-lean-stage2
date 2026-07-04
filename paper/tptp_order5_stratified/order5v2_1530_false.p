% order5v2_1530  eq1=17742 eq2=18486  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(Y,f(Y,Z)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Z),f(Y,f(f(W,X),W))) )).
