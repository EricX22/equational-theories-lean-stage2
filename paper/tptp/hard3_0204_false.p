% hard3_0204  eq1=1890 eq2=1303  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,X)),f(Z,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(X,Z),Z),X)) )).
