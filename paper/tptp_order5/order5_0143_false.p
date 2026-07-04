% order5_0143  eq1=57530 eq2=831  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,X)) = f(f(f(X,Y),X),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(X,Y),f(Z,W))) )).
