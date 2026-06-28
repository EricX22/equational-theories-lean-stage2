% hard3_0204  eq1=1890 eq2=1303  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,X)),f(Z,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(f(X,Z),Z),X)) )).
