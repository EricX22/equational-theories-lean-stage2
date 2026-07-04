% order5v2_1598  eq1=12341 eq2=6319  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),Z),f(W,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(W,f(f(X,Z),Y)))) )).
