% hard3_0233  eq1=2119 eq2=4655  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Z),f(W,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),Y) != f(f(X,Z),Y) )).
