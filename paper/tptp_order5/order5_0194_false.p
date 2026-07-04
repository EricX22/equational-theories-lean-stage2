% order5_0194  eq1=13464 eq2=11660  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [R,U,V,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,f(U,V))),R)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(W,W)),f(Z,Z))) )).
