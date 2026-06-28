% hard3_0085  eq1=644 eq2=2462  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Y),Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(Y,X),Z)),X) )).
