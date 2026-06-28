% hard3_0239  eq1=2156 eq2=1887  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Y),Z),f(W,X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,f(X,X)),f(Y,X)) )).
