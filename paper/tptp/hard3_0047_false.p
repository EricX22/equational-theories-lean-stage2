% hard3_0047  eq1=294 eq2=4155  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,Z),Y),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(f(Y,X),X),Y) )).
