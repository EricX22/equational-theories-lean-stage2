% order5_0104  eq1=15124 eq2=33263  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),f(Y,U)),X)) )).
fof(neg, negated_conjecture, ? [U,V,W,X,Y,Z] : ( X != f(f(Y,f(f(f(Y,Z),W),U)),V) )).
