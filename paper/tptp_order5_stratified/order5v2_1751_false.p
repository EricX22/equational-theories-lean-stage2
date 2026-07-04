% order5v2_1751  eq1=17805 eq2=9901  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(W,f(W,W)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,W),f(W,f(Y,Z)))) )).
