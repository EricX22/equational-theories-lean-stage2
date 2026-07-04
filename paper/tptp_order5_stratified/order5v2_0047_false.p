% order5v2_0047  eq1=4979 eq2=54735  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(Z,f(X,f(Y,W))))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,f(X,X)) != f(Y,f(f(Z,W),U)) )).
