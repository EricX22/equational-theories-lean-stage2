% order5_0238  eq1=9698 eq2=36861  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Z,Y),f(Z,f(X,Z)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),Y),f(X,W)),X) )).
