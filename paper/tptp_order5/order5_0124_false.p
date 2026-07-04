% order5_0124  eq1=2093 eq2=23701  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,X),X),f(Z,X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Z),Y),f(X,f(Y,W))) )).
